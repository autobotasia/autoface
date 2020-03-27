from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
import os
import glob
from .models import TimeKeeping
from django.conf import settings
from faker import Faker
import pandas as pd
import random as rd



def save_record_to_database():

    static_folder = "static/"
    fake = Faker()

    img_list = []
    for img_link in glob.glob(static_folder + 'temp_save/*'):
        # remove "static/"
        img_link = img_link[7:]
        img_list.append(img_link)

    emo_list = []
    for emo_link in glob.glob('static/img/test-ava/emo*'):
        # remove "static/"
        emo_link = emo_link[7:]
        print(emo_link)
        emo_list.append(emo_link)

    for i in range(1000):
        # TimeKeeping(image_link, name, age, emo, last_checkin, last_checkout, prob)
        record = TimeKeeping(image_link=rd.choice(img_list), name=fake.name(), age=rd.randint(1, 80), emo=rd.choice(emo_list), last_checkin=fake.date_time(), last_checkout=fake.date_time(), prob=rd.random())
        print(record)
        record.save()

    print("Finish save_records_to_database.")


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
