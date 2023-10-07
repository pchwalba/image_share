from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import auth
from .validators import validate_image_extension, validate_expiration_time
import time
import uuid
# Create your models here.


class Tier(models.Model):
    name = models.CharField(max_length=20)
    thumbnail_size_small = models.IntegerField()
    thumbnail_size_large = models.IntegerField(null=True, blank=True)
    original_size = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    @property
    def get_thumbnail_sizes(self):
        return self.thumbnail_size_small, self.thumbnail_size_large if self.thumbnail_size_large else 400

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(auth.get_user_model(), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', validators=[validate_image_extension], max_length=255)
    thumbnail_small = models.ImageField(upload_to='images/')
    thumbnail_large = models.ImageField(upload_to='images/')


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="expiring_link", unique=True)
    link = models.CharField(max_length=255)
    expires_in = models.IntegerField(validators=[validate_expiration_time])

    def is_expired(self):
        current_time = time.time()
        return current_time > self.expires_in
