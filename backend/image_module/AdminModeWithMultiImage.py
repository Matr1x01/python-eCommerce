from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from image_module.models import ImageModel


class ImageInline(GenericTabularInline):
    model = ImageModel


class HasAdminImageInlineMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name == 'AdminModeWithMultiImage':
            cls.inlines = list(getattr(cls, 'inlines', [])) + [ImageInline]


class CombinedMeta(HasAdminImageInlineMeta, type(ModelAdmin)):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        fields = getattr(cls, 'fields', None)
        readonly_fields = getattr(cls, 'readonly_fields', [])
        if fields is not None and 'images' in fields and 'images' not in readonly_fields:
            cls.readonly_fields = list(readonly_fields) + ['images']


class AdminModeWithMultiImage(ModelAdmin, metaclass=CombinedMeta):
    def images(self, obj):
        image_section = ""
        for image in obj.images:
            image_section += '<img src="{}" style="width: auto; height: 100px; padding:10px;" />'.format(
                image.get_image_url())
        return format_html(image_section)
