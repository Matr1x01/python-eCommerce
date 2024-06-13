from django.conf.global_settings import MEDIA_ROOT
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from product.models import *

from image_module.models import ImageModel


# class CategoryInline(admin.TabularInline):
#     model = Product.category.through


class ImageInline(GenericTabularInline):
    model = ImageModel


class ProductAdmin(admin.ModelAdmin):

    inlines = [ImageInline]

    def images(self, obj):
        image_section = ""
        for image in obj.images:
            image_section += '<img src="{}" style="width: auto; height: 100px; padding:10px;" />'.format(image.get_image_url())
        return format_html(image_section)

    fields = ('name', 'slug', 'cost_price', 'selling_price', 'description', 'brand', 'category', 'images')
    readonly_fields = ('images',)
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
