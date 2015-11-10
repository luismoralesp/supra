from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import inlineformset_factory, modelformset_factory
from django.http import HttpResponse
from django.db.models import Q
import models
import json

"""
	@name: SuperListView
	@author: exile.sas
	@date: 13/10/2015
	@licence: creative commons
"""
class SupraListView(ListView):
	template_name = "supra/json.html"
	list_display = None

	def dispatch(self, request, *args, **kwargs):
		self.kwargs['q'] = request.GET.get('q', '')
		return super(SupraListView, self).dispatch(request)
	#end def

	def get_queryset(self):
		queryset = super(SupraListView, self).get_queryset()
		if 'q' in self.kwargs:
			serach = self.kwargs['q']
			q = Q()
			for column in self.list_filter:
				kwargs = {
					'{0}__{1}'.format(column, 'icontains'): serach, 
				}
				q = Q(q | Q(**kwargs))
			#end for
			queryset = queryset.filter(q)
		#end if
		if self.list_display:
			return list(queryset.values(*self.list_display))
		#end if
		return list(queryset.values())
	#end def

	def get_context_data(self, **kwargs):
		context = super(SupraListView, self).get_context_data(**kwargs)
		context['num_rows'] = len(context['object_list'])
		context['object_list'] = json.dumps(context['object_list'], cls=DjangoJSONEncoder)
		return context
	#end def

	def render_to_response(self, context, **response_kwargs):
	    return super(SupraListView, self).render_to_response(context, content_type="application/json", **response_kwargs)
    #end def

#end class

class SupraFormView(FormView):
	template_name = "supra/form.html"
	inlines = []
	validated_inilines = []

	def form_valid(self, form):
		instance = form.save()
		for inline in self.validated_inilines:
			inline.instance = instance
			inline.save()
		#end for
		return HttpResponse(status=200)
	#end def

	def get_context_data(self, **kwargs):
		context = super(SupraFormView, self).get_context_data(**kwargs)
		print context
		context['inlines'] = []
		for inline in self.inlines:
			form_class = inline().get_form_class()
			context['inlines'].append(form_class())
		print context['inlines']
		return context
	#end def

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid() and self.is_valid_inlines():
			return self.form_valid(form)
		#end if
		return self.form_invalid(form)
	#end def

	def is_valid_inlines(self):
		for inline in self.inlines:
			i = inline()
			form = i.get_form_class()
			f = form(**self.get_form_kwargs())
			if not f.is_valid():
				return False
			#end if
			self.validated_inilines.append(f)
		#end for
		return True
	#end for

	def form_invalid(self, form):
		errors = dict(form.errors)
		for i in self.inlines:
			errors.update(dict(i.errors))
		#end for
		return HttpResponse(json.dumps(errors), status=400, content_type="application/json", **response_kwargs"application/json")
	#end def
	#end def

#end class

class SupraInlineFormView(SupraFormView):
	base_model = None
	inline_model = None
	formset_class = None
	form_class = None
	
	def get_form_class(self):
		if self.formset_class and self.form_class:
			return inlineformset_factory(self.base_model, self.inline_model, form=self.form_class, formset=self.formset_class, exclude=[], extra=2)
		else:
			return inlineformset_factory(self.base_model, self.inline_model, exclude=[])
		#end if
	#end def
#end class