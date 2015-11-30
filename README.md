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
if you don't want to show JSON keys like *field__subfield*, you can use **Rendere** sub class.

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
```
*Result*
```
[{"friendly": "subvalue", "field2":"value2"}, ...]
```
