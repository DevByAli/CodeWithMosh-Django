from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from .filter import *


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to specify page size
    max_page_size = 100 # Maximum page size allowed
    
  
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
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
    pagination_class = CustomPagination
    
    
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