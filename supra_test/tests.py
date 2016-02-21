from django.test import TestCase
from supra import views as supra
import models
import forms

#supra.SupraConf.body = True

class MyModelListView(supra.SupraListView):
	model = models.MyModel
	list_display = ['field1', 'field2', 'field3']
	search_fields = ['field1', 'field2']
#end class

class MyModelFormView(supra.SupraFormView):
    model = models.MyModel
    form_class = forms.MyModelForm
    template_name = 'MyModelTemplate.html'
#end class

class SupraTest(TestCase):
	def test_list_view(self):
		print "**** SupraListView *****"
		class request():
			method = 'GET'
			GET = {
				"field1": "",
				"field2": "",
				"field3": " ",
			}
			body = '{"field1": "2"}'
		#end class
		
		view = MyModelListView.as_view()
		requ = view.view_class(kwargs={})
		print requ.dispatch(request=request())
		print "************************"
	#end def

	def test_form_view(self):
		print "**** SupraFormView *****"
		view = MyModelFormView.as_view()
		class request():
			method = 'POST'
			POST = {
				'field1': 'value1',
				'field2': 'value2',
				'field3': 'value3'
			}
			body = '{"field1": "value1", "field2": "value2", "field3":"value3"}'
			FILES = {}
		#end class
		requ = view.view_class(request = request())
		print requ.post([])
		print "************************"
		self.test_list_view()
	#end def
#end class


if __name__ == '__main__':
    unittest.main()