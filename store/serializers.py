from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers
from decimal import Decimal
from django.shortcuts import *
from .signals import sig_order_created
from .models import *


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
    
    product_count = serializers.IntegerField(default=0, read_only=True) # read_only make the field not required during creating the collection
    

class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']
        
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        product = get_object_or_404(Product, pk=product_id)
        
        return ProductImage.objects.create(product=product, **validated_data)
    
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product

        # Order of fields matter.
        # Include the fields in 'fields' list if it is customized like 'unit_price_with_tax'
        # NOT RECOMMENDED: fields = '__all__'
        fields = ['id', 'title', 'description', 'unit_price', 'inventory', 'unit_price_with_tax', 'collection', 'images']
        
    unit_price_with_tax = serializers.SerializerMethodField(method_name='get_unit_price_with_tax') # method_name is required when method_name != "get_{field_name}"

    
    def get_unit_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
        
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        
        

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True) # REMEMBER THIS many=True!!!!
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart: Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])
   
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    # validate_{field_name} is the to validate a particular field
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            # More elegant way to raise exception from serializer
            raise Http404("Product of given ID was not found")
        return value
        
    
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        # get_object_or_404(Product, pk=product_id)
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
        

class UpdateCartItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
        

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantiy']
        
        
class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    
    def get_total(self, order: Order):
        return sum([orderitem.product.unit_price * orderitem.quantiy for orderitem in order.items.all()])
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items', 'total']
        

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise Http404("Cart not found.")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise Http404("No item found in cart.")     
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context.get('user_id')
            
            
            customer = Customer.objects.get(user_id=user_id)
            order = Order.objects.create(customer=customer)
            
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantiy=item.quantity,
                    unit_price=item.product.unit_price
                ) for item in cart_items
            ]
            
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()
            
            sig_order_created.send_robust(self.__class__, order=order)
            
            return order