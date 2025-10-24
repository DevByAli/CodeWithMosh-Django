from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.db.models import Count
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
@api_view()
def products_list(request: Request):
    products = get_list_or_404(Product.objects.select_related('collection'))
    # many=True if the queryset contain many objects
    # context is required by the serializer.HyperlinkedRelatedField
    serializer = ProductSerializer(products, many=True, context={'request': request}) 
    
    return Response(data=serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_detail(request: Request, id: int):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        new_product = ProductSerializer(data=request.data)
        new_product.is_valid(raise_exception=True)
        new_product.save()
        return Response(data=new_product.data)
    
    elif request.method == 'PUT':
        update_product = ProductSerializer(product, data=request.data, partial=True) # partial=True means some fields to update
        update_product.is_valid(raise_exception=True)
        update_product.save()
        return Response(data=update_product.data)
    elif request.method == 'DELETE':
        if product.orderitem.count() > 0:
            return Response(
                {"error": "Product cannot delete b/c some of the orderitems associated with it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_list(request: Request):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    collections = get_list_or_404(queryset)
    serilizer = CollectionSerializer(collections, many=True)
    return Response(data=serilizer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PUT'])
def collection_details(request: Request, pk):
    
    queryset = Collection.objects.annotate(product_count=Count('products'))
    collection = get_object_or_404(queryset, pk=pk)
    
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        new_collection = CollectionSerializer(data=request.data)
        new_collection.is_valid(raise_exception=True)
        new_collection.save()
        return Response(data=new_collection.data, status=status.HTTP_201_CREATED)