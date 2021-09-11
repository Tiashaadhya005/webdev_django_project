from sys import maxsize
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100,required=True)
    your_email=forms.EmailField(required=True)
    your_mobile=forms.IntegerField(max_value=9999999999,required=False)
    your_password=forms.CharField(max_length=20)
    