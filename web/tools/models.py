from django.db import models

# Create your models here.
class ImageDetail(models.Model):
    img_url = models.TextField(default='')
    #tag_name = models.TextField()
    file_path = models.TextField()
    top1 = models.TextField()
    top2 = models.TextField()
    top3 = models.TextField()
    visited = models.BooleanField(default=False)
