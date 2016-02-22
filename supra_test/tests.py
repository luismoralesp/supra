from django.test import TestCase
import views

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
		
		view = views.MyModelListView.as_view()
		requ = view.view_class(kwargs={})
		print requ.dispatch(request=request())
		print "************************"
	#end def

	def test_form_view(self):
		print "**** SupraFormView *****"
		view = views.MyModelFormView.as_view()
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