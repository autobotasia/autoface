from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from tools.models import ImageDetail

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

    STATUS_ACTIVE = "Active"
    STATUS_PAUSED = "Paused"
    STATUS_DISABLED = "Disabled"
    STATUS_CHOICES = (
        (STATUS_ACTIVE, "ACTIVE"),
        (STATUS_PAUSED, "PAUSED"),
        (STATUS_DISABLED, "DISABLED")
    )
    camera_title = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)
    IP_camera = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PAUSED)


    def __str__(self):
        status_list = ['ACTIVE', 'PAUSED', 'DISABLED']
        return 'camera: %s\narea: %s\norganization: %s\nIP: %s\nstatus: %s\n' % (self.camera_title, self.area, self.organization_name, self.IP_camera, self.status)


class Organization(models.Model):

    organization_name = models.CharField(max_length=100)
    admin = models.CharField(max_length=100)
    location = models.TextField()
    tel = models.CharField(max_length=15)

    def __str__(self):
        return 'organization: %s\nadmin: %s\nlocation: %s\ntel: %s\n' % (self.organization_name, self.admin, self.location, self.tel)


class GroupOfTitle(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    checkin = models.BooleanField(default=False)
    checkin_time = models.DateTimeField()
    checkout = models.BooleanField(default=False)
    checkout_time = models.DateTimeField()


class UserExtraData(models.Model):

    # Many user to one organization
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField()
    age = models.IntegerField()
    about_me = models.TextField()


class TimeKeeping(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image_detail = models.OneToOneField(ImageDetail, on_delete=models.SET_NULL, null=True)
