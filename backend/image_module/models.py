from django.db import models
import uuid as uuid_lib
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ImageModel(models.Model):
    uuid = models.UUIDField(editable=False, unique=True, default=uuid_lib.uuid4)
    image = models.ImageField(upload_to='images/', null=True)
    title = models.CharField(max_length=100, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    related_primary_key = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'image_module'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def get_absolute_url(self):
        return self.image.url

    def get_image_url(self):
        return self.image.url

    def get_image_path(self):
        return self.image.path

    def get_image_name(self):
        return self.image.name

    def get_image_uuid(self):
        return self.uuid

    @staticmethod
    def get_object_images(object):
        object_id = object.id
        content_type = ContentType.objects.get_for_model(object.__class__)
        return ImageModel.objects.filter(object_id=object_id, content_type=content_type)

    @staticmethod
    def add_object_image(object, image):
        content_type = ContentType.objects.get_for_model(object.__class__)
        return ImageModel.objects.create(image=image, content_type=content_type, object_id=object.id)

    @staticmethod
    def add_object_images(object, images):
        content_type = ContentType.objects.get_for_model(object.__class__)
        return ImageModel.objects.bulk_create([ImageModel(image=image, content_type=content_type, object_id=object.id) for image in images])

    @staticmethod
    def remove_object_image(object, uuid):
        content_type = ContentType.objects.get_for_model(object.__class__)
        return ImageModel.objects.get(uuid=uuid, content_type=content_type, object_id=object.id).delete()

    @staticmethod
    def remove_all_object_images(object):
        content_type = ContentType.objects.get_for_model(object.__class__)
        return ImageModel.objects.filter(content_type=content_type, object_id=object.id).delete()
