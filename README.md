![Logo](https://drive.google.com/uc?export=view&id=0B4P0WGQG9LrDTmVzaVFtZ01EckU)
# supra

It's an easy JSON service generator, using the native django ListView class as base.

##Install##
  sudo python setup.py install

##Use##

###SupraListView###
It's a simple paginater JSON service. It shows a searchable list of registers paginated by an indicated number.

**Fields**
  - *model:* Stipulate the model which will be shown, **it is mandatory**.
  - *list_display:* Stipulate the field list to show of this model.
  - *search_fields:* Stipulate the searchable field list.

**Example**

*models.py*
```python
from django.db import models

class MyModel(models.Model):
  field1 = models.CharField(max_length=45)
  field2 = models.CharField(max_length=45)
  field3 = models.CharField(max_length=45)
#end class
```
*views.py*
```python
import supra
import models

class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['field1', 'field2', 'field3']
  search_fields = ['field1', 'field2']
#end class
```
*urls.py*
```python
from django.conf.urls import include, url
import views

urlpatterns = [
  url(r'mymodel/list/', views.MyModelListView.as_view(), name="mymodel_list"),
]
```
*Result*
```json
{"num_rows": 1, "object_list": [{"field1": "value1", "field2":"value2", "field3":"value3"}]}
```

Also you can use *field__field* instead field name as *list_display* as for *search_fiels*.

*views.py*
```python
import supra
import models

class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['field1__subfield', 'field2',]
#end class
```
*Result*
```json
{"num_rows": 1, "object_list": [{"field1__subfield": "subvalue", "field2":"value2"}]}
```

if you don't want to show JSON keys like *field__subfield*, you can use **Renderer** sub class.

**Renderer**

Sub class Renderer  let you use friendly names for you JSON keys instead *field__subfield*.

*views.py*
```python
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
```json
{"num_rows": 1, "object_list": [{"friendly": "subvalue", "field2":"value2"}]}
```

**Pagination**
You can paginate your service jus using the *paginate_by* attribute like this:

```python
import supra
import models
class MyModelListView(supra.SupraListView):
  model = models.MyModel
  list_display = ['friendly', 'field2',]
  paginate_by = 2
#end class
```

You can use the *page* GET parameter to select which page choose, the page range start with 1

```
/?page=1
```

*Result*
```json
{"count": 5, "num_pages": 3, "object_list": [{"field2": "", "field3": "", "field1": "1"}, {"field2": "", "field3": "", "field1": "2"}], "next": 2, "page_range": "xrange(1, 4)", "num_rows": 2}
```

###SupraFormView###
It's a class based on the native django FormView class, but modified for use JSON as error list response instead of a HTML template.

**fields**
- *model:* Espesify the model which will be created and/or edited, **it is mandatory**.
- *form_class:* Espesify the form class which will create and/or edit the model, **it is mandatory**.
- *template_name:* Espesify the name/path file for render the form template. it is not mandatory, if you do not espesify it, supra will use a generic default template.
- *inlines:* Espesify a **SupraInlineFormView** list for stack in this form.
**Example**

*views.py*
```python
class MyModelFormView(supra.SupraFormView):
	model = models.MyModel
	form_class = forms.MyModelForm
	template_name = 'MyModelTemplate.html'
#end class
```
*MyModelTemplate.html*
```html
<form action="" method="post">{% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Send message" />
</form>
```
on error will show a response like
```json
{"field1":["This field is required."]}
```
##SupraInlineFormView##
**fields**
- *base_model:* Spesify the base model for attach the set of others models, **it is mandatory**.
- *inline_model:* Spesify the model which will be attached on the base model, **it is mandatory**, also is mandatory that the inline model have a relation(ForeignKey, OneToOneField, ...) directly with the base model.
- *form_class:* Spesify the form class which will be used for create the formset.

**Example**


*models.py*
```python
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
```python
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
```html
<form action="" method="post">{% csrf_token %}
    {{form.as_p}}
    {% for fo in inlines %}
    	{{ fo.as_p }}
    {% endfor %}
    <input type="submit" value="Send message" />
</form>
```
on error will show a response like
```json
{"field1":["This field is required."], "inlines":[{"inlinefield": "This field is required."}]}
```
### Body Request ###
The *body request* is not enable by default, but you can enable it using the *body* attribute in *SupraListView* class.

*Example*

```python
class MyModelFormView(supra.SupraFormView):
  model = models.MyModel
  form_class = forms.MyModelForm
  template_name = 'MyModelTemplate.html'
  body = True
#end class
```

Also you can use the *SupraConf* class for configure for all like this

```python
supra.SupraConf.body = True
```

That's all for now folks.
