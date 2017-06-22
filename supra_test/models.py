from django.db import models

class MyModel(models.Model):
	field1 = models.CharField(max_length=45)
	field2 = models.CharField(max_length=45)
	field3 = models.ImageField(upload_to="image")
#end class

class MyInlineModel(models.Model):
	mymodel = models.ForeignKey(MyModel)
	field1 = models.CharField(max_length=45)
	field2 = models.CharField(max_length=45)
	field3 = models.CharField(max_length=45)
#end class

class FotoReporte(models.Model):
	url = models.FileField(upload_to="fotos")
#end class

class Reporte(models.Model):
	nombre = models.CharField(max_length=100)
	tipo_de_reporte = models.IntegerField()
	descripcion = models.TextField(max_length=400)
	fecha = models.DateTimeField(auto_now_add=True)
	foto = models.ImageField(upload_to="images")
	aass = models.FileField(upload_to="aass", blank=True, null=True)
	piscina = models.IntegerField()
	mymodel = models.ForeignKey(MyModel)
	null = models.NullBooleanField(default=None)
	fotos = models.ManyToManyField(FotoReporte)
#end def