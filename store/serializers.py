from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_with_tax = serializers.SerializerMethodField(method_name='get_unit_price_with_tax') # method_name is required when method_name != "get_{field_name}"

    # Ways to serialize relationships #
    
    # First way
    collection_1st_way = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        # read_only=True, # This also works.
        source='collection' # B/c collection_1st_way is a different field name
    )
    
    # Second way
    # This will hit queries for each product. 
    # So, we need to add the select_related('collection') in the product that is passed to this serializer in views.
    collection_2nd_way = serializers.StringRelatedField(source='collection') 


    # Third way
    # This is add the nested_object in product object
    # we also need to add the select_related('collection') in the product that is passed to this serializer in views.
    collection_3rd_way = CollectionSerializer(source='collection')

    
    #Fourth way
    collection_4th_way = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-details',
        source='collection'
    )
    
    def get_unit_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)