from django.contrib import admin

# Register your models here.
from .models import TimeKeeping, Camera, Organization, GroupOfTitle

admin.site.register(TimeKeeping)
admin.site.register(Camera)
admin.site.register(Organization)
admin.site.register(GroupOfTitle)
