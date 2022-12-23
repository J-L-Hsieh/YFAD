from operator import index
from django.contrib import admin
from django.urls import path,re_path
from django.urls import  include

from yeast import views

urlpatterns = [
    path('yeast/search/', include('search.urls')),

    path('',views.home),


    path('yeast/browse',views.yeast),
    path('yeast/ajax_yeast_browser/',views.yeast_browser),
    path('yeast/ajax_associated/',views.yeast_associated),
    path('yeast/browse/associated/',views.yeast_associated_base),
    path('yeast/browse/associated/detail/',views.yeast_name_base),
    path('yeast/ajax_name/',views.yeast_name),
    path('yeast/ajax_modal/',views.yeast_modal),
    path('yeast/ajax_evidence/', views.yeast_evidence),
]
