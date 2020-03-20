from django.urls import path
from . import views

urlpatterns = [
    path('report', views.report, name='account_report'),
    path('crud/<str:arg>/', views.crud, name='account_crud'),
]
