from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_class, name='create_class'),
    path('join', views.join_class, name='join_class'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)