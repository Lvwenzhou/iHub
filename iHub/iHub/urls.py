"""iHub URL Configuration

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
import iHub_site.views as site_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', site_view.login),
    path('logout/', site_view.logout),
    path('my/', site_view.my),
    path('register/', site_view.register),
    path('start_plan/', site_view.start_plan),
    path('plans/', site_view.plans),
    path('take_part/', site_view.take_part),
    path('my_plans/', site_view.my_plans),
    path('cancel_plan/', site_view.cancel_plan),
    path('quit_plan/', site_view.quit_plan),
    path('carpool_index/', site_view.carpool_index),
]
