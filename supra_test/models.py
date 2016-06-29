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

class Reporte(models.Model):
	nombre = models.CharField(max_length=100)
	tipo_de_reporte = models.IntegerField()
	descripcion = models.TextField(max_length=400)
	fecha = models.DateTimeField(auto_now_add=True)
	piscina = models.IntegerField()
	mymodel = models.ForeignKey(MyModel)
#end def

class FotoReporte(models.Model):
	url = models.FileField(upload_to="fotos")
	reporte = models.ForeignKey(Reporte)
#end class