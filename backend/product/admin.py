from django.contrib import admin
from product.models import *


class CategoryInline(admin.TabularInline):
    model = Product.category.through


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('category',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
