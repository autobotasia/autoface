from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class TimeKeeping(models.Model):

    image_link = models.CharField(max_length=150)
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    emo = models.CharField(max_length=50)
    last_checkin = models.DateTimeField()
    last_checkout = models.DateTimeField()
    prob = models.FloatField()
