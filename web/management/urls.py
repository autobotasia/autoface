from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('crud/<str:arg>/<str:opt>', views.crud, name='management_crud'),
    path('', lambda request: redirect('management_report', permanent=True)),
    path('report', views.report, name='management_report'),
    path('camera', views.camera_list, name="camera_list"),
    path('organization', views.organization_list, name='organization_list'),
    path('group-of-title', views.group_of_title_list, name='group_of_title_list'),
]
