from django.urls import path
from . import views

urlpatterns = [
    path('report', views.report, name='management_report'),
    path('crud/<str:arg>/', views.crud, name='management_crud'),
]
