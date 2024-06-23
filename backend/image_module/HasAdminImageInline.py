from django.contrib.contenttypes.admin import GenericTabularInline

from image_module.models import ImageModel


class ImageInline(GenericTabularInline):
    model = ImageModel


class HasAdminImageInlineMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name == 'HasAdminImageInline':
            if not hasattr(cls, 'inlines'):
                cls.inlines = []
            cls.inlines = cls.inlines + [ImageInline]


class HasAdminImageInline(metaclass=HasAdminImageInlineMeta):
    def __init__(self):
        pass
