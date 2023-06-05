from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('upload_video/', views.upload_video, name='upload_video'),
]
