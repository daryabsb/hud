
from django.db import models
from src.core.base import BaseModel
from src.core.modules import upload_image_file_path


class Logo(BaseModel):
    name = models.CharField(max_length=100, default='Zeneon Company Logo')
    image = models.ImageField(null=True, blank=True,
                              default='uploads/logo/7a81a70d-3fe0-4c24-ba80-d1bf7f95b5a0.png',
                              upload_to=upload_image_file_path)

    def __str__(self):
        return self.name
