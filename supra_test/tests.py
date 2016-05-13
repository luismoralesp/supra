from django.test import TestCase
from supra import views as supra
import views
import models
import forms


class SupraTest(TestCase):
	def test_list_view(self):
		print "**** SupraListView *****"
		class request():
			method = 'GET'
			GET = {
				"field1": "",
				"field2": "",
				"field3": "",
			}
			body = '{"field1": "2"}'
		#end class
		print 'GET', request.GET
		view = views.MyModelListView.as_view()
		requ = view.view_class(kwargs={})
		print requ.dispatch(request=request())
		print "************************"
	#end def

	def test_form_view(self):
		print "**** SupraFormView *****"
		view = views.MyModelFormView.as_view()
		class request():
			method = 'PUT'
			POST = {
				'field1': 'value1',
				'field2': 'value2',
				'field3': 'value2',
			}
			#body = '{"field1": "value1", "field2": "value2", "field3":"value3"}'
			FILES = {}
		#end class
		requ = view.view_class(request = request())
		print requ.post([])
		print "************************"
		#self.test_list_view()
	#end def

	def test_form_update_view(self):
		print "**** SupraFormView *****"
		#self.test_form_view()
		view = views.MyModelFormView.as_view()
		class request():
			method = 'PUT'
			POST = {
				'field1': 'edited',
				'field2': 'edited',
				'field3': 'edited',
				'id': 1
			}
			#body = '{"field1": "value1", "field2": "value2", "field3":"value3"}'
			FILES = {}
		#end class
		requ = view.view_class(request = request())
		print requ.post([])
		print "************************"
		#self.test_list_view()
	#end def

	def test_form_get_view(self):
		print "**** SupraFormView GET *****"
		view = views.MyModelFormView.as_view()
		class request():
			method = 'GET'
		#end class
		requ = view.view_class(request = request())
		print "OK", requ.post([]), "OK"
		print "************************"
		#self.test_list_view()
	#end def
#end class


if __name__ == '__main__':
    unittest.main()