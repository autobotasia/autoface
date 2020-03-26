from django.db import models

# Create your models here.
class ImageDetail(models.Model):
    file_path = models.TextField(default='')
    #img_url = models.TextField(default='')
    top1 = models.TextField()
    top2 = models.TextField()
    top3 = models.TextField()
    # tag_name = models.TextField()
    visited = models.BooleanField(default=False)
