from django import forms
from django.forms import ModelForm

from models import *


class PersonForm(ModelForm):
    class Meta:
	model = Person

class RelationShipForm(ModelForm):
    class Meta:
	model = RelationShip
	exclude = ['created_date','modified_date']

class PhoneGroupForm(ModelForm):
    class Meta:
	model = PhoneGroup


class PhoneNumberForm(ModelForm):
    class Meta:
	model = PhoneNumber

class EmailForm(ModelForm):
    class Meta:
	model = Email

class EventForm(ModelForm):
    class Meta:
	model = Event


'''
class PersonForm(forms.Form):
    name = forms.CharField(max_length=75)
    image = forms.ImageField(upload_to='/tmp/', blank=True, null=True)
    groups = forms.ManyToManyField(PhoneGroup, blank=True, null=True, help_text=_('The groups this user belongs to.'))
    organisation = forms.CharField(max_length = 150,  blank=True, null=True)
    relation = forms.ForeignKey(RelationShip,  blank=True, null=True)
    created_date = forms.DateTimeField(auto_now_add=True)
    modified_date = forms.DateTimeField(blank=True, null=True)
'''
