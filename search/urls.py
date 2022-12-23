from operator import index
from django.contrib import admin
from django.urls import path,re_path
from search import views

urlpatterns = [

    path('', views.search_base),
    path('ajax_search/', views.search_mode),

]
