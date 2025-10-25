from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Count
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to specify page size
    max_page_size = 100 # Maximum page size allowed

class ProductList(ListCreateAPIView):
    """
    get and post methods are implemented in ListCreateAPIView that import that 
    ListModelMixin and CreateModelMixin.
    We just need to define the queryset, serializer_class and serializer_context.

    NOTE:
    - Use methods if there is login to get these. e.g; Get the queryset based on the user role etc.
    - get the serializer based on the login user role.
    """
    
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    
    
    def delete(self, request: Request, pk: int):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem.count() > 0:
            return Response(
                {"error": "Product cannot delete b/c some of the orderitems associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer



class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer
    
    
    def delete(self, request: Request, pk: int):
        collection = get_object_or_404(self.queryset, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {"error": "Collection cannot delete b/c some of the products associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)