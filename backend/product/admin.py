from django.contrib import admin
from product.models import * 


class CategoryInline(admin.TabularInline):
    model = Product.category.through 

class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('category',)


admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)