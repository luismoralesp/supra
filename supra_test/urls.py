"""
"""
from django.conf.urls import patterns, include, url
from supra import views as supra
from django.views.generic.base import TemplateView
import views
from django.contrib.admin import site

from django.shortcuts import render_to_response
from django.template import RequestContext


urlpatterns = [

    url(r'^admin/', site.urls),
	url(r'reporte/list/$', views.ReporteView.as_view()),
	url(r'reporte/form/(?P<pk>\d+)/', views.ReporteFormView.as_view()),
	url(r'oauth/', TemplateView.as_view(template_name='oath.html'))
]


