from django.db import models
from src.core.modules import upload_image_file_path


class Migration(models.Model):
    version = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    file_name = models.FileField(
        null=True, blank=True, upload_to=upload_image_file_path
    )
    module = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Version:{self.version} | on: ({self.created})"
