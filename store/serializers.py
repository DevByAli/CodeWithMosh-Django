from rest_framework import serializers
from .models import Product
from decimal import Decimal

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_with_tax = serializers.SerializerMethodField(method_name='get_unit_price_with_tax') # method_name is required when method_name != "get_{field_name}"
    
    def get_unit_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)