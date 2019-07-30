from django import forms

class SearchUserForm(forms.Form):
    email = forms.CharField(label="Email", max_length = 200)
    password = forms.CharField(label="Password",max_length=30)