"""hofvidz URL Configuration

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
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path, include
from halls import views
from tags import views as tag_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    #AUTH
    path('signup',views.SignUp.as_view(), name='signup'),
    path('login',auth_views.LoginView.as_view(),name='login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    #hall - crud
    path('halloffame/create', views.CreateHall.as_view(), name='create_hall'),
    path('halloffame/<int:pk>', views.ViewHall.as_view(), name='view_hall'),
    path('halloffame/<int:pk>/update', views.UpdateHall.as_view(), name='update_hall'),
    path('halloffame/<int:pk>/delete', views.DeleteHall.as_view(), name='delete_hall'),
    path('halloffame/<int:pk>/save', views.SavehallView.as_view(), name='save_hall'),
    path('user/<int:pk>/',views.userdetail,name='user_dash'),

    #Video
    path('halloffame/<int:pk>/addvideo', views.VideoAddView.as_view(), name='addvideo'),
    path('halloffame/<int:pk>/deletevideo', views.DeleteVideo.as_view(), name='deletevideo'),
    path('video/search', views.video_search, name='video_search'),
    path('hall/search', views.hall_search, name='hall_search'),

    path('api/halls/',include(('halls.api.urls','halls'), namespace='halls-api')),
    path('api/tags/',include(('tags.api.urls','tags'), namespace='tags-api')),
    path('tags/<tag>',tag_view.TagsView.as_view(), name='tags-view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)