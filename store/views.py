from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.mixins import *
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *
from .serializers import *
from .filter import *
from .pagination import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
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
class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    'prefetch_related' is used for one-to-many relations
    'select_related' is used for one-to-one relations 
    """
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer