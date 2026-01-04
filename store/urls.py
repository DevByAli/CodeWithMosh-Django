from django.urls import path
from rest_framework_nested import routers
from pprint import pprint
from . import views


router = routers.DefaultRouter()

# `basename` actually used by django for naming the url list product-list, product-detail

router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet)
router.register('customer', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

"""
DOCS: for nested router search here: https://github.com/alanjds/drf-nested-routers
"""
product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
product_router.register('images', views.ProductImageViewSet, basename='product-images')

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + product_router.urls + cart_router.urls

pprint(urlpatterns)
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-details') # pk added b/c serializers.HyperlinkedRelatedField interally looking for 'pk' lookup_field
# ]
