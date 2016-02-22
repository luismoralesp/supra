"""
"""
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'mymodel/$', views.MyModelListView.as_view()),
	url(r'mymodel/form/$', views.MyModelFormView.as_view()),
)


