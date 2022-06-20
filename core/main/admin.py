from django.contrib import admin
from .models import Product, Category, Brand, Customer, Cart, CartItems, ShippingAddress


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(ShippingAddress)

