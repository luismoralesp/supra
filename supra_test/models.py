from django.db import models


class MyModel(models.Model):
	field1 = models.CharField(max_length=45)
	field2 = models.CharField(max_length=45)
	field3 = models.CharField(max_length=45)
#end class

class MyInlineModel(models.Model):
	mymodel = models.ForeignKey(MyModel)
	field1 = models.CharField(max_length=45)
	field2 = models.CharField(max_length=45)
	field3 = models.CharField(max_length=45)
#end class