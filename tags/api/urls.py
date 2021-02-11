from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path, include
from tags import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    TagListAPIView
)

urlpatterns = [
    path('', TagListAPIView.as_view(), name='list'),
]