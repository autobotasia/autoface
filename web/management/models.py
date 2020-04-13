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


class Camera(models.Model):

    camera_title = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)
    IP_camera = models.CharField(max_length=20)
    status = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])


class Organization(models.Model):

    organization_name = models.CharField(max_length=100)
    admin = models.CharField(max_length=100)
    location = models.TextField()
    tel = models.CharField(max_length=15)


class GroupOfTitle(models.Model):

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    checkin = models.BooleanField(default=False)
    checkin_time = models.DateTimeField()
    checkout = models.BooleanField(default=False)
    checkout_time = models.DateTimeField()
