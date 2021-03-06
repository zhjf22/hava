"""hava URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from havaApp import views
import django.contrib.auth.views as auth_views ##不要忘记导入这个


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index/', views.index),
    path('submit/', views.index_submit),
    path('show_log/', views.show_log),
    path('approve/',views.approve),
    path('login/', views.login),
    path('app_exec',views.app_exec)
]
