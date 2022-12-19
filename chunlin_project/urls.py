from operator import index
from django.contrib import admin
from django.urls import path,re_path
from yeast import views

urlpatterns = [
    # path('', views.index),
    # path('wormbase/',views.wormbase),
    # path('pirscan/',views.pirscan),
    # path('pirscan/search/',views.PirScan),

    # path('search/',views.search),
    # path('search/ajax_mode1/',views.mode1),
    # path('detail/ajax_detail/',views.ajax_crawler),
    # re_path(r'detail/(?P<pk>.+)/',views.detail),


    # path('web_tool/ajax_wormbase/', views.ajax_wormbase),
    # path('web_tool/ajax_data/', views.ajax_data),
    # path('web_tool/ajax_crawler/', views.ajax_crawler),

    # path('browser/',views.browser),
    # path('browser/ajax_browser/',views.browser_type),

    # path('enrichment/',views.enrichment),
    # path('enrichment/ajax_enrichment/',views.enrichment_analysis),
    # re_path(r'enrichment/(?P<pk>.+)/',views.domain),
    # path('enrichment/ajax_domain/',views.domain_data),

    path('',views.yeast),
    path('yeast/ajax_yeast_browser/',views.yeast_browser),
    path('yeast/ajax_associated/',views.yeast_associated),
    path('yeast/associated/',views.yeast_associated_base),
    path('yeast/associated/detail/',views.yeast_name_base),
    path('yeast/ajax_name/',views.yeast_name),
    path('yeast/ajax_modal/',views.yeast_modal),

]
