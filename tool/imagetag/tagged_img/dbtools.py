from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
import os
import glob
from .models import ImageDetail
from django.conf import settings


def loc_save2db():

    base_dir = 'static'

    for dir1 in os.listdir(base_dir):
        if dir1 == 'css':
            continue

        base_dir1 = base_dir + '/' + dir1
        for dir2 in os.listdir(base_dir1):
            base_dir2 = base_dir1 + '/' + dir2
            for img_file in os.listdir(base_dir2):
                img_url = dir1 + '/' + dir2 + '/' + img_file
                try:
                    img = get_object_or_404(ImageDetail, img_url=img_url)
                except Http404:
                    img = ImageDetail(img_url=img_url, tag_name=dir2)
                    img.save()


def save_img_data_to_database():

    base_dir = './static/' + settings.TEMP_IMG
    print(base_dir)
    # img name: Nguyen_Van_A_<time>.png
    for img_link in glob.glob(base_dir + '*/*'):
        img_name = img_link.split('/')[-1]
        # tag_name = '_'.join(img_name.split('_')[:-1])
        tag_name = img_link.split('/')[-2]
        print(settings.TEMP_IMG + tag_name + '/' + img_name)
        img = ImageDetail(img_url=settings.TEMP_IMG + tag_name + '/' + img_name, tag_name=tag_name)
        img.save()

    print("Finish save_img_data_to_database.")


def delete_all():

    print('delete all function')
    img_list = get_list_or_404(ImageDetail)
    for img in img_list:
        img_url = img.img_url
        img.delete()
        print("Deleted ", img_url + '.')


def delete_img(img_pk):

    print('delete all function')
    img = get_object_or_404(ImageDetail, pk=img_pk)
    img_url = img.img_url
    img.delete()
    print("Deleted ", img_url + '.')


def reset_visited_value():

    img_list = get_list_or_404(ImageDetail, visited=True)
    if img_list == 404:
        print("Here")
    for img in img_list:
       img.visited = False
       img.save()
