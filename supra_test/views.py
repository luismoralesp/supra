from supra import views as supra
import models
import forms


supra.SupraConf.body = False
supra.SupraConf.template = False
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
