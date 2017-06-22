from django import forms
import models

class MyModelForm(forms.ModelForm):
	class Meta:
		model = models.MyModel
		fields = []
#end class

class ReporteForm(forms.ModelForm):
	class Meta:
		model = models.Reporte
		exclude = []
	# end def
# edn def