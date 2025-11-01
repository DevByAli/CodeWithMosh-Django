from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'product_count']
    
    product_count = serializers.IntegerField(default=0, read_only=True) # read_only make the field not required during creating the collection
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        # Order of fields matter.
        # Include the fields in 'fields' list if it is customized like 'unit_price_with_tax'
        # NOT RECOMMENDED: fields = '__all__'
        fields = ['id', 'title', 'description', 'unit_price', 'inventory', 'unit_price_with_tax', 'collection']
        
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
        