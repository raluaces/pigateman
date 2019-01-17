from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('open/', views.ajax_door, name="ajax_door" ),
    path('', views.landing, name="landing")
]