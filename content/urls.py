from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("home", views.index, name='home'),
    path("anasayfa", views.index),


    path("start_scan/", views.start_scan, name="start_scan"),
    path("update_table/", views.update_table, name="update_table"),

    path('update_output_info/', views.update_output_info, name='update_output_info'),
]

