from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_per_page = 10

    @admin.display(ordering="collection__title")
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "product_count"]

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["description", "discount"]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "membership", "orders"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    
    @admin.display(ordering='orders')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({"customer__id": str(customer.id)})
        )
        
        return format_html('<a href={}>{}</a>',url, customer.orders)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["street", "city", "customer"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["placed_at", "payment_status", "customer"]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantiy", "unit_price"]


# Register your models here.
# admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Collection, CollectionAdmin)
# admin.site.register(models.OrderItem, OrderItemAdmin)
# admin.site.register(models.Order, OrderAdmin)
# admin.site.register(models.Promotion, PromotionAdmin)
# admin.site.register(models.Customer, CustomerAdmin)
# admin.site.register(models.Address, AddressAdmin)
