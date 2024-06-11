from django.db import models
import uuid
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 


class ImageModel(models.Model):
    uuid = models.UUIDField(editable=False, unique=True,
                            null=False, blank=False)
    image = models.ImageField(upload_to='images/', null=True)
    title = models.CharField(max_length=100, null=True)
    content_Type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    related_primary_key = GenericForeignKey("content_type", "object_id")
    path = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'image_module'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        # indexes = [
        #     models.Index(fields=["content_type", "object_id"]),
        # ]

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

    def get_related_model(self):
        apps.get_model(self.related_app, self.related_model)

    def get_related_object(self):
        model = self.get_related_model()
        return model.objects.get(pk=self.related_primary_key)

    def create(self, image, related_primary_key, related_app, related_model, path):
        uuid = uuid.uuid4()
        self.uuid = uuid
        self.image = image
        self.title = str(uuid)
        self.related_primary_key = related_primary_key
        self.related_app = related_app
        self.related_model = related_model
        self.path = path
        self.save()
