from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products_list),
    path('products/<int:id>/', views.product_detail),
    path('collection/<int:pk>', views.collection_details, name='collection-details') # pk added b/c serializers.HyperlinkedRelatedField interally looking for 'pk' lookup_field
]
