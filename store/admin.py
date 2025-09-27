from django.contrib import admin
from . import models



class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory", "collection"]

class CollectionAdmin(admin.ModelAdmin):
    # list_display = ["title"]
    pass

class PromotionAdmin(admin.ModelAdmin):
    list_display = ["description", "discount"]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "membership"]


class AddressAdmin(admin.ModelAdmin):
    list_display = ["street", "city", "customer"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["placed_at", "payment_status", "customer"]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantiy", "unit_price"]
    
    
# Register your models here.
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Address, AddressAdmin)
