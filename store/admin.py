from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory", "collection"]
    list_editable = ['unit_price']
    list_per_page = 10
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # list_display = ['title']
    pass
    
@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["description", "discount"]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "membership"]
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    

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
