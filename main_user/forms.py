from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=10)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    password = forms.CharField(min_length=4)
