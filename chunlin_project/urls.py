from operator import index
from django.contrib import admin
from django.urls import path,re_path
from django.urls import  include

from yeast import views

urlpatterns = [
    path('search/', include('search.urls')),

    path('',views.home),


    path('browse',views.yeast),
    path('ajax_yeast_browser/',views.yeast_browser),
    path('ajax_associated/',views.yeast_associated),
    path('browse/associated/',views.yeast_associated_base),
    path('browse/associated/detail/',views.yeast_name_base),
    path('ajax_name/',views.yeast_name),
    path('ajax_modal/',views.yeast_modal),
    path('ajax_evidence/', views.yeast_evidence),
]
