"""
"""
from django.conf.urls import patterns, include, url
from supra import views as supra
from django.views.generic.base import TemplateView
import views

from django.shortcuts import render_to_response
from django.template import RequestContext

def some_view(request):
	return render_to_response('websocket.html', {}, context_instance=RequestContext(request))
#end def

urlpatterns = [
	url(r'', include(supra.all_supras(views))),
	url(r'ws/', some_view)#TemplateView.as_view(template_name='websocket.html'))
]


