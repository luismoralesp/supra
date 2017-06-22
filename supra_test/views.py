from supra import views as supra
from supra.auths import methods, oauth
import models
import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

supra.SupraConf.body = True
supra.SupraConf.template = False
supra.SupraConf.ACCECC_CONTROL["allow"] = True
supra.SupraConf.ACCECC_CONTROL["origin"] = "http://192.168.1.12:4200"

#methods.append(oauth.SupraOAuth)

"""
class MyInlineModelListView(supra.SupraListView):
	model = models.MyInlineModel
	list_display = ['field1', 'field2', 'field3', 'id', 'friendly']
	list_filter  = ['field1', 'field2']
	paginate_by  = 2

	class Renderer:
		friendly = 'mymodel__id'
	#end class
#end class

class MyInlineFormView(supra.SupraInlineFormView):
	model = models.MyInlineModel
	base_model = models.MyModel

#end class

class MyModelListView(supra.SupraListView):
	model = models.MyModel
	list_display = ['field1', 'field2', 'field3', 'id']
	list_filter  = ['field1', 'field2']
	paginate_by  = 2
#end class

class MyModelFormView(supra.SupraFormView):
	model = models.MyModel
#end class
"""
import json
class MyModelDetailView(supra.SupraDetailView):
	model = models.MyModel
	template_name = "supra/form.html"
# end def

class MyModelListView(supra.SupraListView):
	model = models.MyModel
	list_display = ['field1', 'field2', 'field3', 'id', ('material', 'json')]
	list_filter  = ['field1', 'field2']
	paginate_by  = 2

	def material(self, obj, row):
		class request():
			method = 'GET'
			GET = {}
		# end class
		material = MyModelDetailView(dict_only=True).dispatch(request=request(), pk='1')
		print material
		return json.dumps(material)
	# end def
#end class

class Login(supra.SupraSession):
	body = False
# end class

class MyModelCRUD(supra.SupraCRUD):
	model = models.MyModel
	#inlines = [MyInlineFormView]
	auto_inlines = [models.MyInlineModel]

	def get_queryset(self):
		queryset = super(type(MyModelCRUD), self).get_queryset()
		queryset = queryset.filter(field2="")
		return queryset
	# end def

#end class

class FotoFormView(supra.SupraInlineFormView):
	model = models.FotoReporte
	base_model = models.Reporte
#end class

class FotoFormView2(supra.SupraFormView):
	model = models.FotoReporte
#end class

class ReporteView(supra.SupraListView):
	model = models.Reporte
	list_display = ['nombre', 'mymodel__field1', 'null', ('title', 'json'), 'foto', 'aass']
	#search_fields = ['nombre', 'descripcion']
	search_key = 'q'
	
	def title(self, obj, row):
		return '[{"hola":"%s"}]' % (obj.nombre, )
	# end def

	def get_queryset2(self):
		queryset = super(ReporteView, self).get_queryset()
		return queryset.extra({'e': 'select \'{"11":"11"}\''})
	# end def
#end class

class ReporteFormView(supra.SupraFormView):
	response_json = True
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(ReporteFormView, self).dispatch(request, *args, **kwargs)
	#end def

	model = models.Reporte
	form_class = forms.ReporteForm
# end class
from django.http import HttpResponse

@supra.access_control
def is_login(request):
	return HttpResponse(str(request.user))
# end def