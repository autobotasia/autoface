from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.conf import settings
from random import randrange
import os
import shutil
from .models import ImageDetail
from . import dbtools


# Create your views here.
def detail(request, img_id):

    img = get_object_or_404(ImageDetail, pk=img_id)
    tags = settings.TAG_LIST
    return render(request, 'detail.html', {
        'imagedetail': img,
        'tags': tags,
    })


def vote(request, img_id):

    try:
        img = get_object_or_404(ImageDetail, pk=img_id)
        check = request.POST['check']
        # if check == 'False':
        #     tag_name = request.POST['tagname']
        #     tag_name.replace(' ', '_')
        #     if tag_name not in settings.TAG_LIST:
        #         messages.warning(request, 'Tên không có trong danh sách.', extra_tags='alert')
        #         return HttpResponseRedirect(reverse('detail', args=(img.pk,)))

        #     # Update data in database
        #     img.tag_name = tag_name

        if check == 'True':
            img.visited = True
            img.save()

            # copy to class folder
            img_url = './static/' + img.img_url
            path = './saved/' + img.tag_name + '/'
            img_dir = path + os.path.basename(img_url)
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copyfile(img_url, img_dir)

        img_list = get_list_or_404(ImageDetail, visited=False)
    except Http404:
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('detail', args=(img_list[randrange(len(img_list))].pk,)))


def home(request):

    try:
        img_list = get_list_or_404(ImageDetail, visited=False)
    except Http404:
        return HttpResponse("No image.")
    else:
        img = get_object_or_404(ImageDetail, pk=img_list[randrange(len(img_list))].pk)
        tags = settings.TAG_LIST
        return render(request, 'detail.html', {
            'imagedetail': img,
            'tags': tags,
        })


@login_required
def crud(request, arg, img_pk=0):

    if arg == "reset-visited-value":
        try:
            dbtools.reset_visited_value()
            print("Finish reset")
        except Http404:
            return HttpResponse("Reset visited value successful.")
        else:
            return HttpResponse("Reset visited value successful.")
    elif arg == "delete":
        try:
            dbtools.delete_img(img_pk)
        except Http404:
            return HttpResponse('Not found image data has primary key =', img_pk)
        else:
            return HttpResponse("Deleted image " )
    elif arg == "delete-all":
        try:
            dbtools.delete_all()
        except :
            pass
        finally:
            return HttpResponse("Delete all successfully.")
    elif arg == "save-image-data-to-database":
        dbtools.save_img_data_to_database()
        return HttpResponse("Saved all image data object to database.")

    return HttpResponse("Argument is not valid.")
