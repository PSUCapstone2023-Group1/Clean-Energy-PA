from django import forms


class RegisterUser(forms.Form):
    name = forms.CharField(label="Name", max_length=80)
    email = forms.CharField(label="Email", max_length=80, required=False)
    username = forms.CharField(label="Username", max_length=80, required=False)
    password = forms.CharField(label="Password", max_length=80, required=False)
