from django.urls import path
from rest_framework_nested import routers
from pprint import pprint
from . import views


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)

"""
DOCS: for nested router search here: https://github.com/alanjds/drf-nested-routers
"""
product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + product_router.urls

pprint(urlpatterns)
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-details') # pk added b/c serializers.HyperlinkedRelatedField interally looking for 'pk' lookup_field
# ]
