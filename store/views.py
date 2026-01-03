from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import *
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermissions
from .models import *
from .serializers import *
from .filter import *
from .pagination import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    # pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    # filterset_fields = ['collection_id', 'inventory']

    
    def get_serializer_context(self):
        return {'request': self.request}
    
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Product cannot delete b/c some of the orderitems associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    
    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(products__collection=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Collection cannot delete b/c some of the products associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() # This is returning all the reviews in db 
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product__id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']} # This is the loopup=product in urls, here 'product' is the prefix

"""
We don't want the update, list feature. So only import these.
"""
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    'prefetch_related' is used for one-to-many relations
    'select_related' is used for one-to-one relations 
    """
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH': # Only want to update single field
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects \
                .select_related('product') \
                .filter(cart_id=self.kwargs['cart_pk'])
                

class CustomerViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    
    # This is the rule base permissions
    # def get_permissions(self):
    #     if self.request.user.is_staff:
    #         return [IsAdminUser()]
    #     if self.action == 'me':
    #         return [IsAuthenticated()]

    #     if self.request.method == 'GET':
    #         return [AllowAny()] # REMEMBER!!! Pass the object AllowAny() not class AllowAny
    #     return [IsAuthenticated()]
    

    # if detail=True means http://localhost:8000/store/customer/{customer_id}/me/
    # else details=False means http://localhost:8000/store/customer/me/
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request: Request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
            
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data)
        
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermissions])
    def history(self, request, **kwargs):
        pk = kwargs.get('pk')
        return Response(f"History of user {pk}")
    
    
class OrderViewSet(ModelViewSet):
    # This restricts the request method
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    # No longer need this function b/c we are not relying on mixin `create` methog   
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}
    
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.prefetch_related('items__product').all()
        
        if user.is_staff:
            return queryset
        
        # Here `get_or_create` is voilating the Command Query Principle.
        # Command Query Principle: Says either the method query data or perform any operation 
        # in a particular method not do both. 
        # We will come later and will fix it.
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return queryset.filter(customer_id=customer_id)