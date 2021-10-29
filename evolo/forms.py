from django.forms import ModelForm
from django import forms
from .models import VariableMaster,VariableResults
from django.contrib.auth.forms import UserCreationForm
import datetime


class VariableMasterForm(ModelForm):
    """create new varible for tracking"""
    class Meta:
        model = VariableMaster
        fields = ['variable_name','variable_type','person']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['person'].widget = forms.HiddenInput()


class VariableResultsForm(ModelForm):
    class Meta:
        model = VariableResults
        fields = ['result_numeric','result_binary','result_categorical','result_scale']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['result_categorical'].widget.attrs['class'] = 'form-control'
        self.fields['result_numeric'].widget.attrs['class'] = 'form-control'
        self.fields['result_scale'].widget.attrs['class'] = 'form-control'
        self.fields['result_scale'].widget.attrs['placeholder'] = '1 - 10'

        if self.instance.variable.variable_type == VariableMaster.NUMERIC:

            self.fields['result_binary'].widget = forms.HiddenInput()
            self.fields['result_categorical'].widget = forms.HiddenInput()
            self.fields['result_scale'].widget = forms.HiddenInput()
        elif self.instance.variable.variable_type == VariableMaster.BINARY:

            self.fields['result_numeric'].widget = forms.HiddenInput()
            self.fields['result_categorical'].widget = forms.HiddenInput()
            self.fields['result_scale'].widget = forms.HiddenInput()
        elif self.instance.variable.variable_type == VariableMaster.CATEGORICAL:

            self.fields['result_numeric'].widget = forms.HiddenInput()
            self.fields['result_binary'].widget = forms.HiddenInput()
            self.fields['result_scale'].widget = forms.HiddenInput()
        elif self.instance.variable.variable_type == VariableMaster.SCALE:

            self.fields['result_numeric'].widget = forms.HiddenInput()
            self.fields['result_binary'].widget = forms.HiddenInput()
            self.fields['result_categorical'].widget = forms.HiddenInput()




class NewUserForm(UserCreationForm):
    """New user registration form"""
    def __init__(self,*args,**kwargs):
        super(NewUserForm, self).__init__(*args,**kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
