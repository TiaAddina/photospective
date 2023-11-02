from django.forms import ModelForm
from .models import Image


# Based on Django's documentation for file uploads via ModelForms:
# https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['imagepath']
