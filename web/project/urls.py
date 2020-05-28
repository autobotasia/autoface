"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# from users import views as user_views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url

admin.site.site_header = "NCC Admin"
admin.site.site_title = "NCC Admin Portal"
admin.site.index_title = "Welcome to NCC Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tools.urls')),
    # path('register/', user_views.register, name='register'),
    # path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login', RedirectView.as_view(url='/admin/login/?next=/admin/', permanent=True), name='login'),
    path('logout', TemplateView.as_view(template_name='logout.html'), name='logout'),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/signup/$',registration_views.UserSignUp.as_view(),name="signup"),
    path('password-recovery', TemplateView.as_view(template_name='password-recovery.html'), name='password-recovery'),

    path('management/', include('management.urls'), name="management"),
    path('404error', TemplateView.as_view(template_name='404.html'), name='404-url'),
]
