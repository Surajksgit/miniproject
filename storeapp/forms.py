# forms.py
from django import forms
from .models import login,Signup

class AddForm(forms.ModelForm):
    class Meta:
        model = login

        fields = "__all__"

class AddForm(forms.ModelForm):
    class Meta:
        model = Signup

        fields = "__all__"


