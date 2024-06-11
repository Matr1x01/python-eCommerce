from django.conf.global_settings import MEDIA_ROOT
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from product.models import *


# class CategoryInline(admin.TabularInline):
#     model = Product.category.through


class ImageInline(GenericTabularInline):
    model = ImageModel




class ProductAdmin(admin.ModelAdmin):

    # inlines = [ImageInline]

    def image_tag(self, obj):
        if obj.images:
            return format_html('<img src="{}" style="width: auto; height: 100px;" />'.format(MEDIA_ROOT+obj.images.url))
        return "No Image"

    fields = ('name', 'slug', 'cost_price', 'selling_price', 'description', 'brand', 'category', 'image_tag')
    readonly_fields = ('image_tag',)
    filter_horizontal = ('category',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: auto; height: 100px;" />'.format(MEDIA_ROOT+obj.logo.url))
        return "No Image"
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description', 'image_tag', 'logo')
    readonly_fields = ('image_tag',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
