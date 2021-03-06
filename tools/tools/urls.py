from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:Id>', views.detail, name='detail'),
    path('detail/<int:Id>/vote', views.vote, name='vote'),
    path('crud/<str:arg>/', views.crud, name='crud'),
    path('crud/<str:arg>/<int:img_pk>', views.crud, name='crud'),
    
]
