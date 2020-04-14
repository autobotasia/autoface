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

    # STATUS_ACTIVE = 0
    # STATUS_PAUSED = 1
    # STATUS_DISABLED = 2
    camera_title = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)
    IP_camera = models.CharField(max_length=20)
    status = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])

    def __str__(self):
        status_list = ['ACTIVE', 'PAUSED', 'DISABLED']
        return 'camera: %s\narea: %s\norganization: %s\nIP: %s\nstatus: %s\n' % (self.camera_title, self.area, self.organization_name, self.IP_camera, status_list[self.status])


class Organization(models.Model):

    organization_name = models.CharField(max_length=100)
    admin = models.CharField(max_length=100)
    location = models.TextField()
    tel = models.CharField(max_length=15)

    def __str__(self):
        return 'organization: %s\nadmin: %s\nlocation: %s\ntel: %s\n' % (self.organization_name, self.admin, self.location, self.tel)


class GroupOfTitle(models.Model):

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    checkin = models.BooleanField(default=False)
    checkin_time = models.DateTimeField()
    checkout = models.BooleanField(default=False)
    checkout_time = models.DateTimeField()

    def __str__(self):
        return 'name: %s\nposition: %s\ntitle: %s\ncheckin: %s\ncheckin_time: %s\ncheckout: %s\ncheckout_time: %s\n' % (self.name, self.position, self.title, str(self.checkin), str(self.checkin_time), str(self.checkout), str(self.checkout_time))
