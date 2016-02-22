"""
"""
from django.conf.urls import patterns, include, url
<<<<<<< HEAD
import views

urlpatterns = patterns('',
	url(r'mymodel/$', views.MyModelListView.as_view()),
	url(r'mymodel/form/$', views.MyModelFormView.as_view()),
=======

urlpatterns = patterns('',
>>>>>>> master
)


