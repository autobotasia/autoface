from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from . import mock_dbtools
from .models import TimeKeeping
# Create your views here.
# @login_required
def report(request):

    try:
        data_list = get_list_or_404(TimeKeeping)
        # paginator = Paginator(data_list, 25)
        #
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        page_obj = data_list

        return render(request, 'report.html', {
            "page_obj": page_obj,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


def camera_list(request):
    try:
        return render(request, 'camera-list.html')
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


def organization_list(request):
    try:
        return render(request, 'organization-list.html')
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


def group_of_title_list(request):
    try:
        return render(request, 'group-of-title.html')
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


def crud(request, arg, img_pk=0):

    if arg == "save-record-to-database":
        try:
            mock_dbtools.save_record_to_database()
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
