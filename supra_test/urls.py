"""
"""
from django.conf.urls import include, url
from supra import views as supra
from django.views.generic.base import TemplateView
import views
from django.contrib.admin import site

from django.shortcuts import render_to_response
from django.template import RequestContext
from supra.views import all_supras
import models

urlpatterns = [

    url(r'^admin/', site.urls),
	url(r'^reporte/list/$', views.ReporteView.as_view()),
	url(r'^reporte/form/(?P<pk>\d+)/', views.ReporteFormView.as_view()),
	url(r'^reporte/form/', views.ReporteFormView.as_view()),
	url(r'^foto/form/', views.FotoFormView2.as_view()),
	url(r'^usuarios/login/$', views.Login.as_view()),
	url(r'^crud/', views.MyModelCRUD.as_view()),
	url(r'^usuarios/is/login/$', views.is_login),
	url(r'^d/(?P<pk>\d+)/$', views.MyModelDetailView.as_view()),
	url(r'^list/$', views.MyModelListView.as_view()),
	url(r'^oauth/', TemplateView.as_view(template_name='oath.html'))
]


