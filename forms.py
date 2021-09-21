from sys import maxsize
import warnings
from django import forms
from django.core.exceptions import ValidationError


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100,required=True)
    your_email=forms.EmailField(required=True)
    your_mobile=forms.IntegerField(max_value=9999999999,required=False)
    your_password=forms.CharField(max_length=8,min_length=5,widget = forms.PasswordInput, 
                                error_messages = {'required':"Password should contain a special character from '@' '#' '%''$'"})

    def clean_your_password(self):
        #the password have to contain any special character from "@#$%"
        value = self.cleaned_data["your_password"]
        len_value=len(value)
        special_flag=0
        special_char="$&%#"
        for i in range(len_value):
            if value[i] in special_char:
                special_flag=1
        if special_flag==1:
            return value
        else:
            raise ValidationError("Password should contain a special character from '@' '#' '%''$'")
        
##doubt:-> alert message for password field    
