from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    path('crud/<str:arg>/<str:opt>', views.database_crud, name='management_crud'),
    path('', lambda request: redirect('management_report', permanent=True)),
    path('report', views.report, name='management_report'),

    path('camera', views.camera_list, name="camera_list"),
    path('camera/', lambda request: redirect('camera_list', permanent=True)),
    path('camera/create', views.camera_create, name='camera_create'),
    path('camera/<int:id>/<str:opt>', views.camera_crud, name="camera_crud"),

    path('organization', views.organization_list,    name='organization_list'),
    path('organization/', lambda request: redirect('organization_list', permanent=True)),
    path('organization/create', views.organization_create, name='organization_create'),
    path('organization/<int:id>/<str:opt>', views.organization_crud, name="organization_crud"),

    path('group-of-title', views.group_of_title_list, name='group_of_title_list'),
]
