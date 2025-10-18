from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@api_view()
def products_list(request: Request):
    products = get_list_or_404(Product.objects.select_related('collection'))
    # many=True if the queryset contain many objects
    # context is required by the serializer.HyperlinkedRelatedField
    serializer = ProductSerializer(products, many=True, context={'request': request}) 
    
    return Response(data=serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request: Request, id: int):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        product = ProductSerializer(data=request.data)
        
        if product.is_valid():
            product.validated_data
            return Response('ok')
        else:
            return Response(data=product.errors)



@api_view()
def collection_details(request: Request, pk: int):
    return Response('ok')