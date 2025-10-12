from django.contrib import admin, messages
from . import models
from django.db.models import Count, QuerySet
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory' # Filter title
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'), # (parameter_value, Filter Value)
            ('<20', 'Medium')
        ]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '<20':
            return queryset.filter(inventory__lt=20, inventory__gt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    exclude = ['promotions'] # Only include exlude these fields
    # fields = ['title', 'slug'] # Only includes these fields
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering="collection__title")
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        elif product.inventory < 20:
            return "Medium"
        return "Ok"
    
    
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ["title", "product_count"]
    search_fields = ['title']

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
    actions = ['delete_orders']
    list_display = ["first_name", "last_name", "email", "membership", "orders"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name", "last_name"]
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'orders']
    
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


    @admin.action(description="Delete Orders")
    def delete_orders(self, request, queryset: QuerySet):
        orders = models.Order.objects.filter(customer__in=queryset)
        order_items = models.OrderItem.objects.filter(order__in=orders)
        
        delete_count = orders.count()
        
        order_items.delete()
        orders.delete()
        
        self.message_user(
            request,
            f"{delete_count} orders of customers deleted successfully.",
            messages.SUCCESS
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
