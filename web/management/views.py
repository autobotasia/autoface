from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from .models import TimeKeeping
from .models import Camera
from .models import Organization
from .models import GroupOfTitle

from . import mock_dbtools
# Create your views here.


# @login_required
def report(request):

    try:
        data_list = get_list_or_404(TimeKeeping)
        # paginator = Paginator(data_list, 25)
        #
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        return render(request, 'report.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


# @login_required
def camera_list(request):
    try:
        data_list = get_list_or_404(Camera)
        return render(request, 'camera-list.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


# @login_required
def organization_list(request):
    try:
        data_list = get_list_or_404(Organization)
        return render(request, 'organization-list.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


# @login_required
def group_of_title_list(request):
    try:
        data_list = get_list_or_404(GroupOfTitle)
        return render(request, 'group-of-title.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


# @login_required
def crud(request, arg, opt):

    if arg == "save-record-to-database":
        try:
            mock_dbtools.save_record_to_database(opt)
        except Http404:
            return HttpResponse("404 Error.")
        else:
            return HttpResponse("Saved all fake records to database.")
    # elif arg == "delete":
    #     try:
    #         dbtools.delete_img(img_pk)
    #     except Http404:
    #         return HttpResponse('Not found image data has primary key =', img_pk)
    #     else:
    #         return HttpResponse("Deleted image " )
    # elif arg == "delete-all":
    #     try:
    #         dbtools.delete_all()
    #     except :
    #         pass
    #     finally:
    #         return HttpResponse("Delete all successfully.")

    return HttpResponse("Argument is not valid.")
