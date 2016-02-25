from supra import views as supra
import models
import forms

supra.SupraConf.body = False
supra.SupraConf.template = False

class MyModelListView(supra.SupraListView):
	model = models.MyModel
	list_display = ['field1', 'field2', 'field3', 'id']
	search_fields = ['field1', 'field2']
	paginate_by = 2
#end class

class MyModelFormView(supra.SupraFormView):
    model = models.MyModel
    form_class = forms.MyModelForm
#end class