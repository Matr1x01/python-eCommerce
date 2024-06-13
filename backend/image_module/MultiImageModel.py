from django.db import models

from image_module.models import ImageModel


class MultiImageModel:

    @property
    def images(self):
        return ImageModel.get_object_images(self).all()

    @property
    def first_image(self):
        return ImageModel.get_object_images(self).first()

    @property
    def first_image_url(self):
        return self.first_image.image.url if self.first_image else None

    @property
    def image_urls(self):
        return [image.image.url for image in self.images]

    @property
    def image_count(self):
        return self.images.count()

    @property
    def has_images(self):
        return self.image_count > 0

    @property
    def has_multiple_images(self):
        return self.image_count > 1

    @property
    def has_single_image(self):
        return self.image_count == 1

    def add_image(self, image):
        return ImageModel.add_object_image(self, image)

    def add_images(self, images):
        return ImageModel.add_object_images(self, images)

    def remove_image(self, uuid):
        return ImageModel.remove_object_image(self, uuid)

    def remove_all_images(self):
        return ImageModel.remove_all_object_images(self)
