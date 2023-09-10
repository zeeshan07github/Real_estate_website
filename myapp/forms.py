from django import forms
from .models import *



class addnewproperty(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = '__all__'

class addnewagent(forms.ModelForm):
    
    class Meta:
        model = AgentProfile
        fields = '__all__'



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class PropertyFilterForm(forms.Form):
    min_price = forms.IntegerField(label='Minimum Price', required=False)
    max_price = forms.IntegerField(label='Maximum Price', required=False)
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        label='Property Type',
        required=False
    )
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='Location',
        required=False
    )
