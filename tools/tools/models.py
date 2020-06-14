from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class ImageDetail(models.Model):

    file_path = models.TextField(default='')
    image_name = models.CharField(max_length=70, null=True)
    time_created = models.DateTimeField(default=timezone.now)
    top1 = models.TextField(default='')
    top1_prob = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    top2 = models.TextField(default='')
    top2_prob = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    top3 = models.TextField(default='')
    top3_prob = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_prob = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    # tag_name = models.TextField()
    # visited = models.BooleanField(default=False)
