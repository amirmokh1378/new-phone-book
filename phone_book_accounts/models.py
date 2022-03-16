from django.db import models
from django.contrib.auth.models import AbstractUser
import os


# Create your models here.

def set_name_and_folder_user_image_file(instance, filename):
    base_name, extension = os.path.splitext(filename)
    return f'image_file/{instance.username}{extension}'


class CustomUser(AbstractUser):
    text = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=set_name_and_folder_user_image_file, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()
