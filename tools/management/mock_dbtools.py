from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
import os
import glob
from .models import TimeKeeping
from .models import Camera
from .models import Organization
from .models import GroupOfTitle
from django.conf import settings
from faker import Faker
import random as rd
import string

STATIC_FOLDER = "static/"

img_list = []
for img_link in glob.glob(STATIC_FOLDER + 'temp_save/*'):
    # remove "static/"
    img_link = img_link[7:]
    img_list.append(img_link)
print("Finish getting img list.")


emo_list = []
for emo_link in glob.glob('static/img/test-ava/emo*'):
    # remove "static/"
    emo_link = emo_link[7:]
    emo_list.append(emo_link)
print("Finish getting emo list.")

fi = open('static/province_list', 'r')
VN_province_list = [line.strip() for line in fi]
print("Finish getting province list.")

print("Create faker object.")
fake = Faker()
print("Finish creating faker object.")


def save_record_to_database(opt):

    if opt == "timekeeping":

        for i in range(1000):
            # TimeKeeping(image_link, name, age, emo, last_checkin, last_checkout, prob)
            record = TimeKeeping(image_link=rd.choice(img_list), name=fake.name(), age=rd.randint(1, 80), emo=rd.choice(emo_list), last_checkin=fake.date_time(), last_checkout=fake.date_time(), prob=rd.random())
            #print(record)
            record.save()

        print("Finish creaing TimeKeeping fake data.")
    #
    elif opt == "camera":

        # STATUS_ACTIVE = 0
        # STATUS_PAUSED = 1
        # STATUS_DISABLED = 2

        for i in range(100):
            camera_title =  ''.join(rd.choice(string.ascii_letters) for _ in range(12))
            area = rd.choice(VN_province_list)
            organization_name = fake.company()
            IP_camera = fake.ipv4()
            status = rd.choice([0, 1, 2])
            record = Camera(camera_title=camera_title, area=area, organization_name=organization_name, IP_camera=IP_camera, status=status)
            print(record)
            record.save()
        print("Finish creating Camera fake data.")


    elif opt == "organization":

        for _ in range(100):
            organization_name = fake.company()
            admin = fake.name()
            location = rd.choice(VN_province_list)
            tel = fake.phone_number()
            record = Organization(organization_name=organization_name, admin=admin, location=location, tel=tel)
            record.save()
        print("Finish creating Organization fake data.")

    elif opt == "group-of-title":

        for _ in range(100):
            name = fake.name()
            position = rd.choice(VN_province_list)
            title = fake.job()
            checkin = rd.choice([False, True])
            checkin_time = fake.date_time()
            checkout = rd.choice([False, True])
            checkout_time = fake.date_time()
            record = GroupOfTitle(name=name, position=position, title=title, checkin=checkin, checkin_time=checkin_time, checkout=checkout, checkout_time=checkout_time)
            record.save()
            print(record)
        print("Finish creating Organization fake data.")
# def delete_all():
#
#     print('delete all function')
#     img_list = get_list_or_404(TimeKeeping)
#     for img in img_list:
#         img_url = img.img_url
#         img.delete()
#         print("Deleted ", img_url + '.')
#
#
# def delete_record(record_pk):
#
#     print('delete all function')
#     img = get_object_or_404(TimeKeeping, pk=img_pk)
#     img_url = img.img_url
#     img.delete()
#     print("Deleted ", img_url + '.')
#
#
# def update_record(record_pk):
#
#     img_list = get_list_or_404(TimeKeeping, visited=True)
#     if img_list == 404:
#         print("Here")
#     for img in img_list:
#        img.visited = False
#        img.save()
