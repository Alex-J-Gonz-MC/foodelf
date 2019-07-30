from django import forms

class NewTableForm(forms.Form):
    server_name = forms.CharField(label="Server Name", max_length = 200)
    table_number = forms.CharField(label="Table Number", max_length=3)
    host_name = forms.CharField(label="Host Name",max_length= 50)