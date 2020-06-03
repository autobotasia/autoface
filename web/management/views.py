from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView, ListView, DeleteView
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TimeKeeping, Camera, Organization, GroupOfTitle
from .forms import CameraForm, OrganizationForm
from . import mock_dbtools
# Create your views here.




@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def camera_list(request):
    try:
        data_list = get_list_or_404(Camera)
        return render(request, 'camera-list.html', {
            "page_obj": data_list,
            "notif": None,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def camera_view(request, id):
    camera = Camera.objects.get(pk=id)
    form = CameraForm(instance=camera)
    return render(request, 'camera-view.html', {'form' : form})
    # return render(request, 'camera-view.html', {'camera' : camera})


@login_required(login_url='/accounts/login/')
@staff_member_required(login_url='refuse_access')
def camera_crud(request, id, opt):

    if opt == 'delete':
        try:
            camera = get_object_or_404(Camera, pk=id)

            if request.method == 'POST':
                camera.delete()
                messages.success(request, 'Deleted camera ' + str(id))
                return HttpResponseRedirect('camera_list')

            return render(request, 'camera-delete.html', {'pk': id, 'camera_name' : camera.camera_title})

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

    else:
        try:
            data_list = get_list_or_404(Camera)
            return render(request, 'camera-list.html', {
                "page_obj": data_list,
            })
        except  Http404:
            print("Http404 Error. Cannot get TimeKeeping Records.")


@login_required(login_url='/accounts/login/')
def organization_list(request):
    try:
        data_list = get_list_or_404(Organization)
        return render(request, 'organization-list.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def organization_view(request, id):

    organization = Organization.objects.get(pk=id)
    form = OrganizationForm(instance=organization)
    return render(request, 'organization-view.html', {'id': id, 'form' : form})


@login_required(login_url='/accounts/login/')
@staff_member_required(login_url='refuse_access')
def organization_crud(request, id, opt):

    if opt == 'delete':
        try:
            organization = get_object_or_404(Organization, pk=id)

            if request.method == 'POST':
                organization.delete()
                messages.success(request, 'Deleted camera ' + str(id))
                return HttpResponseRedirect('organization_list')

            return render(request, 'organization-delete.html', {'pk': id, 'organization_name' : organization.organization_name})

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

        return render(request, 'organization-crud.html', {'id': id, 'form': form})

    else:
        try:
            data_list = get_list_or_404(Organization)
            return render(request, 'organization-list.html', {
                "page_obj": data_list,
            })
        except  Http404:
            print("Http404 Error. Cannot get TimeKeeping Records.")


@login_required(login_url='/accounts/login/')
def group_of_title_list(request):
    try:
        data_list = get_list_or_404(GroupOfTitle)
        return render(request, 'group-of-title.html', {
            "page_obj": data_list,
        })
    except  Http404:
        print("Http404 Error. Cannot get TimeKeeping Records.")


@login_required(login_url='/accounts/login/')
@staff_member_required(login_url='refuse_access')
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


@login_required(login_url='/accounts/login/')
def get_user_profile(request, id):

    user = User.objects.get(pk=id)
    return render(request, 'user-profile.html', { 'id': id, 'form' : form})
