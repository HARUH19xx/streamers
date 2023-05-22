from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('crud_videos/', include("crud_videos.urls")),
    path('users/', include("users.urls")),
]
