"""
"""
from django.conf.urls import patterns, include, url
import views

urlpatterns = [
	url(r'', include(views.MyModelCRUD.as_view())),
]


