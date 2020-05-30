from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from .models import TimeKeeping
from .models import Camera
from .models import Organization
from .models import GroupOfTitle
from .forms import CameraForm
from .forms import OrganizationForm
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
            "notif": None,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


# @login_required
def camera_list(request):
    try:
        data_list = get_list_or_404(Camera)
        return render(request, 'camera-list.html', {
            "page_obj": data_list,
            "notif": None,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


def camera_create(request):

    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            form.save()
            camera_name = form.cleaned_data['camera_title']
            messages.success(request, "Created " + camera_name)
            return HttpResponseRedirect(request.path_info)
    else:
        form = CameraForm()
        return render(request, 'camera-create.html', {'form': form})


# @login_required
def camera_crud(request, id, opt):

    if opt == 'delete':
        try:
            data_list = get_list_or_404(Camera)
            data = get_object_or_404(Camera, pk=id)
            print(data)
            notif = "Deleted camera " + str(data.id)
            return HttpResponseRedirect(reverse('camera_list', args={
                "page_obj": data_list,
                "notif": notif,
            }))
        except  Http404:
            print("Http404 Error. Cannot get TimeKeeping Records.")

    elif opt == 'update':
        camera = get_object_or_404(Camera, pk=id)
        form = CameraForm(instance=camera)

        if request.method == 'POST':
            form = CameraForm(request.POST, instance=camera)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated camera ' + str(id))
                return HttpResponseRedirect(request.path_info)

        return render(request, 'camera-crud.html', {'form': form})

    elif opt == 'view':
        camera = Camera.objects.get(pk=id)
        return render(request, 'temp-camera-view.html', {'camera' : camera})
    else:
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


def organization_create(request):

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            organization_name = form.cleaned_data['organization_name']
            messages.success(request, "Created " + organization_name)
            return HttpResponseRedirect(request.path_info)
    else:
        form = OrganizationForm()
        return render(request, 'organization-create.html', {'form': form})


def organization_crud(request, id, opt):

    if opt == 'delete':
        try:
            data_list = get_list_or_404(Organization)
            data = get_object_or_404(Organization, pk=id)
            print(data)
            notif = "Deleted organization " + str(data.id)
            return HttpResponseRedirect(reverse('organization_list', args={
                "page_obj": data_list,
                "notif": notif,
            }))
        except  Http404:
            print("Http404 Error. Cannot get TimeKeeping Records.")

    elif opt == 'update':
        organization = get_object_or_404(Organization, pk=id)
        form = OrganizationForm(instance=organization)

        if request.method == 'POST':
            form = OrganizationForm(request.POST, instance=organization)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated organization ' + str(id))
                return HttpResponseRedirect(request.path_info)

        return render(request, 'organization-crud.html', {'form': form})

    elif opt == 'view':
        organization = Organization.objects.get(pk=id)
        return render(request, 'temp-organization-view.html', {'organization' : organization})
    else:
        try:
            data_list = get_list_or_404(organization)
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
def database_crud(request, arg, opt):

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
