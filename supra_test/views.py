from supra import views as supra
from supra.auths import methods, oauth
import models
import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

supra.SupraConf.body = False
supra.SupraConf.template = False
supra.SupraConf.ACCECC_CONTROL["allow"] = True

methods.append(oauth.SupraOAuth)

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


class MyModelCRUD(supra.SupraCRUD):
	model = models.MyModel
	#inlines = [MyInlineFormView]
	auto_inlines = [models.MyInlineModel]

#end class

class FotoFormView(supra.SupraInlineFormView):
	model = models.FotoReporte
	base_model = models.Reporte
#end class

class ReporteView(supra.SupraListView):
	model = models.Reporte
	search_fields = ['nombre', 'descripcion']
	
	def title(self, row):
		return row.nombre + row.descripcion
	# end def
#end class

class ReporteFormView(supra.SupraFormView):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(ReporteFormView, self).dispatch(request, *args, **kwargs)
	#end def

	model = models.Reporte
	inlines = [FotoFormView]
# end class
