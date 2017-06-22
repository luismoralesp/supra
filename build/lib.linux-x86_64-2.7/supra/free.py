import json

"""
	@name: SupraConf
	@author: exile.sas
	@date: 21/02/2016
	@licence: creative commons
"""

class SupraConf:
	body = False
	template = False
	date_format = "%d/%m/%Y"
	datetime_format = "%d/%m/%Y %I:%M%p"

	ACCECC_CONTROL = {
		"allow": False,
		"origin": "*",
		"credentials": " true",
		"headers": "accept, content-type",
		"max_age": "1728000",
		"methods": "POST, GET, OPTIONS"
	}
#end class


class FreeList(object):
	def get_context_data(self, **kwargs):
		object_list = self.get_queryset()

		context = {
			'object_list' : [],
			'page_obj': None,
			'paginator': None,
			'num_rows': 0,
			'object_list': object_list
		}
		return context
	# end def

	def get_queryset(self):
		return {}
	# end def

	def dispatch(self, request, *args, **kwargs):
		response_kwargs = {
		}
		context = self.get_context_data(**kwargs)

		return self.render_to_response(context, **response_kwargs)
	# end def
# end class

class HttpResponseBase(object):
	def __call__(self, obj, content_type="text/html"):
		return obj
	# end def
# end class

HttpResponse = HttpResponseBase()

class Request(object):
	method = 'GET'
	GET = {}
# end def


"""
	@name: SupraListView
	@author: exile.sas
	@date: 13/10/2015
	@licence: creative commons
"""
class SupraListView(FreeList):
	list_display = None
	search_fields = []
	list_filter = []
	kwargs = {}
	dict_only = False
	rules = {}
	template = False
	template_name = "supra/list.html"
	request = None
	search_key = 'search'
	date_format = SupraConf.date_format
	datetime_format = SupraConf.datetime_format

	@classmethod
	def as_url(cls):
		app = cls.model.__name__.lower()
		return url('%s/list/$' % (app, ), cls.as_view(),)
	#end class

	def __ini__(self, dict_only = False, *args, **kwargs):
		self.dict_only = dict_only
		return super(SupraListView, self).__init__(*args, **kwargs)
	#end def

	def dispatch(self, request, *args, **kwargs):
		"""
		auth = self.auth(request, *args, **kwargs)
		if auth:
			return auth
		# end if
		"""
		kwargs = self.get_list_kwargs(request)
		self.template = request.GET.get('template', SupraConf.template)
		self.request = request
		return super(SupraListView, self).dispatch(request, *args, **kwargs)
	#end def

	def get_kwargs(self, request):
		kwargs = {}
		if request.method in ('GET',):
			kwargs = request.GET
		#end def
		return kwargs
	#end def

	def get_list_kwargs(self, request):
		kwargs = self.get_kwargs(request)
		for field in self.list_filter:
			if field in kwargs:
				kwarg = kwargs[field]			
				self.kwargs[field] = kwarg
			#end if
		#end for
		if self.search_key in kwargs:
			self.kwargs[self.search_key] = kwargs[self.search_key]
		#end def
		return kwargs
	#end def

	def get_queryset(self):
		queryset = super(SupraListView, self).get_queryset()
		q = Q()
		for column in self.list_filter:
			if column in self.kwargs:
				filter = self.kwargs[column]
				kwargs = {
					column: filter,
				}
				q = Q(q & Q(**kwargs))
			#end if
			queryset = queryset.filter(q)
		#end for
		q = False
		if self.search_key in self.kwargs:
			for column in self.search_fields:
				search = self.kwargs[self.search_key]
				kwargs = {
					'{0}__{1}'.format(column, 'icontains'): search, 
				}
				if q:
					q = q | Q(**kwargs)
				else:
					q = Q(**kwargs)
				# end if
			#end for
			queryset = queryset.filter(q)
		#end if
		queryset = queryset.filter(**self.rules)
		return queryset
	#end def

	def get_context_data(self, **kwargs):
		context = super(SupraListView, self).get_context_data(**kwargs)
		context['num_rows'] = context['object_list'].count()
		context['object_list'] = context['object_list']
		return context
	#end def

	def get_object_list(self, object_list):
		queryset = object_list
		self_list = []
		list_display = []
		if self.list_display:
			for display in self.list_display:
				if hasattr(self, display):
					self_list.append(display)
				else:
					list_display.append(display)
				# end def
			# end for
			if hasattr(self, 'Renderer'):
				renderers = dict((key, F(value)) for key, value in self.Renderer.__dict__.iteritems() if not callable(value) and not key.startswith('__'))
				queryset = queryset.annotate(**renderers)
			#end if
		#end if
		def extra(dct, obj):
			for slf in self_list:
				attr = getattr(self, slf)
				if callable(attr):
					dct[slf] = attr(obj)
				else:
					dct[slf] = attr
				# end if
			# end for
			return dct
		# end def
		return self.format_json(queryset, extra, list_display=list_display)
	#end def

	@classmethod
	def format_json(cls, rows, extra=None, time=0, list_display=[]):
		
		object_list = []

		class OD(object):
			pass
		# end class

		obj = OD()
		for row in rows:
			dct = {}
			pk = row.pk
			row = row.__dict__
			row['pk'] = pk
			for col in row:
				if (not col in ['_state']) and (list_display == [] or col in list_display):
					if isinstance(row[col], datetime.datetime):
						dct[col] = row[col].strftime(cls.datetime_format)
					elif isinstance(row[col], datetime.date):
						dct[col] = row[col].strftime(cls.date_format)
					elif isinstance(row[col], dict):
						dct[col] = cls.format_json(row[col], extra, time=time + 1)
					elif isinstance(row[col], models.Model):
						dct[col] = unicode(row[col])
					else:
						dct[col] = row[col]
					# end if
					setattr(obj, col, dct[col])
				# end if
			# end for
			if extra and callable(extra):
				dct = extra(dct, obj)
			# end if
			object_list.append(dct)
		# end for
		return object_list
	# end def

	def render_to_response(self, context, **response_kwargs):
		json_dict = {}

		object_list = self.get_object_list(context["object_list"])

		page_obj = context["page_obj"]
		paginator = context["paginator"]
		num_rows = context["num_rows"]
		if page_obj:
			if page_obj.has_previous():
				json_dict["previous"] = page_obj.previous_page_number()
			#end if
			if page_obj.has_next():
				json_dict["next"] = page_obj.next_page_number()
			#endif
		#end if
		if paginator:
			json_dict["count"] = paginator.count
			json_dict["num_pages"] = paginator.num_pages
			json_dict["page_range"] = str(paginator.page_range)
		#end if
		json_dict["num_rows"] = num_rows
		json_dict["object_list"] = object_list
		if self.dict_only:
			return json_dict
		#end if
		if self.template:
			json_dict['search_fields'] = self.search_fields
			return render(self.request, self.template_name, json_dict)
		#end if
		httpresponse = HttpResponse(json.dumps(json_dict), content_type="application/json")
		if SupraConf.ACCECC_CONTROL['allow']:
			httpresponse["Access-Control-Allow-Origin"] = SupraConf.ACCECC_CONTROL['origin'];
			httpresponse["Access-Control-Allow-Credentials"] = SupraConf.ACCECC_CONTROL['credentials'];
			httpresponse["Access-Control-Allow-Headers"] = SupraConf.ACCECC_CONTROL['headers'];
			httpresponse["Access-Control-Max-Age"] = SupraConf.ACCECC_CONTROL['max_age'];
			httpresponse["Access-Control-Allow-Methods"] = SupraConf.ACCECC_CONTROL['methods'];
		#end if
		return httpresponse
	#end def

#end class

print SupraListView().dispatch(Request())