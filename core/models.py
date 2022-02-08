from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from solo.models import SingletonModel


class CustomUser(AbstractUser):
    pass


class RemoteSystemSettings(SingletonModel):
    remote_system_base_url = models.URLField()
    aws_access_key_id = models.CharField(max_length=300)
    aws_secret_access_key = models.CharField(max_length=300)
    aws_bucket_name = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        cache.delete("remote_system_base_url")
        cache.delete("aws_access_key_id")
        cache.delete("aws_secret_access_key")
        cache.delete("aws_bucket_name")
        print("----- Cleared The Cache from save !!! -----")
        super().save(*args, **kwargs)
