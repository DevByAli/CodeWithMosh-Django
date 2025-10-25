from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Count
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    """
    get and post methods are implemented in ListCreateAPIView that import that 
    ListModelMixin and CreateModelMixin.
    We just need to define the queryset, serializer_class and serializer_context.
    """
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    # def get(self, request: Request):
    #     queryset = Product.objects.select_related('collection')
    #     products = get_list_or_404(queryset)
    #     serializer = ProductSerializer(products, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    
    # def post(self, request: Request):
    #     new_product = ProductSerializer(data=request.data)
    #     new_product.is_valid(raise_exception=True)
    #     new_product.save()
    #     return Response(data=new_product.data)


class ProductDetail(APIView):
    def get(self, request: Request, id: int):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
    
    
    def put(self, request: Request, id: int):
        product = get_object_or_404(Product, pk=id)
        update_product = ProductSerializer(product, data=request.data, partial=True) # partial=True means some fields to update
        update_product.is_valid(raise_exception=True)
        update_product.save()
        return Response(data=update_product.data)
    
    
    def delete(self, request: Request, id: int):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem.count() > 0:
            return Response(
                {"error": "Product cannot delete b/c some of the orderitems associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CollectionList(APIView):
    def get(self, request: Request):
        queryset = Collection.objects.annotate(product_count=Count('products'))
        collections = get_list_or_404(queryset)
        serilizer = CollectionSerializer(collections, many=True)
        return Response(data=serilizer.data, status=status.HTTP_200_OK)
        
        
    def post(self, request: Request):
        new_collection = CollectionSerializer(data=request.data)
        new_collection.is_valid(raise_exception=True)
        new_collection.save()
        return Response(data=new_collection.data, status=status.HTTP_201_CREATED)



class CollectionDetail(APIView):
    def get(self, request: Request, pk: int):
        queryset = Collection.objects.annotate(product_count=Count('products'))
        collection = get_object_or_404(queryset, pk=pk)
        serilizer = CollectionSerializer(collection)

        return Response(data=serilizer.data)