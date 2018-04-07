from django.db import models
from django.forms import ModelForm
# Create your models here.

class Sheet(models.Model):
	sheet_name = models.CharField(max_length=50)
	sheet_file = models.FileField(upload_to='files')
	
	def __str__(self):
		return self.sheet_name

class SheetForm(ModelForm):
	class Meta(object):
		model = Sheet 
		fields = '__all__'