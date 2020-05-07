from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    path('crud/<str:arg>/<str:opt>', views.crud, name='management_crud'),
    path('', lambda request: redirect('management_report', permanent=True)),
    path('report', views.report, name='management_report'),

    path('camera', views.camera_list, name="camera_list"),
    path('camera/create3', TemplateView.as_view(template_name="camera-create.html"), name='camera_create'),
    path('camera/create', views.camera_create, name='camera_create'),
    path('camera/create2', views.camera_create2, name='camera_create2'),
    path('camera/update', TemplateView.as_view(template_name="camera-crud.html"), name='camera_update'),
    path('camera/<int:id>/<str:opt>', views.camera_crud, name="camera_crud"),

    path('organization', views.organization_list, name='organization_list'),
    path('organization/create', views.organization_create, name='organization_create'),
    path('organization/create2', views.organization_create2, name='organization_create2'),
    path('organization/<int:id>/<str:opt>', views.organization_crud, name="organization_crud"),
    path('organization/create2', TemplateView.as_view(template_name="organization-create.html"), name='organization_create2'),
    path('organization/update', TemplateView.as_view(template_name="organization-crud.html"), name='organization_update'),

    path('group-of-title', views.group_of_title_list, name='group_of_title_list'),
]
