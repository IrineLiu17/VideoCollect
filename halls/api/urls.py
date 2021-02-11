from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path, include
from halls import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    HallListAPIView,
    LikeToggleAPIView
)

urlpatterns = [
    path('', HallListAPIView.as_view(), name='list'),
    path('<int:pk>/save', LikeToggleAPIView.as_view(), name='togglesave'),
]