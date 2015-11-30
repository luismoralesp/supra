# supra

It's an easy JSON services generator, using the native django ListView as base.

##Install##
  not yet, just copy and paste

##Use##

###SupraListView###
It's a simple paginater JSON service. It shown a searchable list of registers paginated by an indicated number.

**Fields**
  - *model:* Spesify the model which will be shown, **it is mandatory**.
  - *list_display:* Spesify the field list to show of this model.
  - *search_fields:* Spesify the searchable field list.

**Example**

*models.py*
```
from django.db import models

class MyModel(models.Model):
  field1 = models.CharField(max_length=45)
  field2 = models.CharField(max_length=45)
  field3 = models.CharField(max_length=45)
#end class
```
*views.py*
```
import supra
import models

class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['field1', 'field2', 'field3']
  search_fields = ['field1', 'field2']
#end class
```
*urls.py*
```
from django.conf.urls import include, url
import views

urlpatterns = [
  url(r'mymodel/list/', views.MyModelListView.as_view(), name="mymodel_list"),
]
```
*Result*
```
[{"field1": "value1", "field2":"value2", "field3":"value3"}, ...]
```

Also you can use *field__field* instead field name as *list_display* as *search_fiels*.

*views.py*
```
import supra
import models

class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['field1__subfield', 'field2',]
#end class
```
*Result*
```
[{"field1__subfield": "subvalue", "field2":"value2"}, ...]
```
if you don't want to show JSON keys like *field__subfield*, you can use **Renderer** sub class.

**Renderer**

Renderer sub class let you use friendlys name for you JSON keys instead *field__subfield*.

*views.py*
```
import supra
import models

class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['friendly', 'field2',]
  class Renderer:
    friendly = 'field1__subfield'
  #end class
#end class
```
*Result*
```
[{"friendly": "subvalue", "field2":"value2"}, ...]
```
###SupraFormView###
It's a class based in the native django FormView class, but modified for use JSON as error list response instead a HTML template.

**fields**
- *model:* Espesify the model which will be created and/or edited, **it is mandatory**.
- *form_class:* Espesify the form class which will create and/or edit the model, **it is mandatory**.
- *template_name:* Espesify the name/path file for render the form template. it is not mandatory, if you not espasify it supra will use a generic default template.
- *inlines:* Espesify a **SupraInlineFormView** list for stack in this form.
**Example**

*views.py*
```
class MyModelFormView(supra.SupraFormView):
	model = models.MyModel
	form_class = forms.MyModelForm
	template_name = 'MyModelTemplate.html'
#end class
```
*MyModelTemplate.html*
```
<form action="" method="post">{% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Send message" />
</form>
```
on error will show a response like
```
{"field1":["This field is required."]}
```
##SupraInlineFormView##
**fields**
- *base_model:* Spesify the base model for attach the set of others models, **it is mandatory**.
- *inline_model:* Spesify the model which will be attached on the base model, **it is mandatory**, also is mandatory that the inline model have a relation(ForeignKey, OneToOneField, ...) directly with the base model.
- *form_class:* Spesify the form class which will be used for create the formset.

**Example**


*models.py*
```
from django.db import models

class MyModel(models.Model):
  field1 = models.CharField(max_length=45)
  field2 = models.CharField(max_length=45)
  field3 = models.CharField(max_length=45)
#end class

class MyInlineModel(models.Model):
  mymodel = models.ForeignKey(MyModel)
  inlinefield = models.CharField(max_length=45)
#end class
```
*views.py*
```
class MyInlineModelFormView(supra.SupraInlineFormView):
	base_model = models.MyModel
	inline_model = models.MyInlineModel
	form_class = forms.MyInlineModelForm
#end class

class MyModelFormView(supra.SupraFormView):
	model = models.MyModel
	form_class = forms.MyModelForm
	template_name = 'MyModelTemplate.html'
	inlines = [MyInlineModelFormView]
#end class
```
*MyModelTemplate.html*
```
<form action="" method="post">{% csrf_token %}
    {{form.as_p}}
    {% for fo in inlines %}
    	{{ fo.as_p }}
    {% endfor %}
    <input type="submit" value="Send message" />
</form>
```
