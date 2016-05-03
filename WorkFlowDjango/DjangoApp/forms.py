from django import forms
from DjangoApp.models import *

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()
    # list_display = ["__unicode__","pub_date"]


class InitialString(forms.Form):
    input_string = forms.CharField(max_length=100)

class NodeFieldsData(forms.ModelForm):
    # list_display = ["__unicode__","pub_date"]
    class Meta:
        model = Node_Data
        fields = ['name','group']

