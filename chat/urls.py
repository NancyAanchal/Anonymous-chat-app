from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lobby/create_lobby/', views.create_lobby, name='create_lobby'),
    path('lobby/', views.lobby, name='lobby')
    
]