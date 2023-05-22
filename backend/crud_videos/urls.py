from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_data, name='get_data'),
    path('hello/', views.hello_view, name='hello_view'),
]