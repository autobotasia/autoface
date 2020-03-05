from django.db import models

# Create your models here.
class ImageDetail(models.Model):
    img_url = models.TextField(default='')
    tag_name = models.TextField()
    visited = models.BooleanField(default=False)
