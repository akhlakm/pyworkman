"""
URL configuration for backend project.

"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .main import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', index, name='main'),
    path("", TemplateView.as_view(template_name='main.html')),
]
