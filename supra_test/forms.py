from django import forms
import models

class MyModelForm(forms.ModelForm):
	class Meta:
		model = models.MyModel
		exclude = []
#end class