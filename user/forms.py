from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=13, required=True)
    last_name = forms.CharField(max_length=13, required=True)
    password = forms.CharField(max_length=20, required=True)

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True)
