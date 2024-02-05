from django import forms

class RegisterUserForm(forms.Form):
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=40)
    surname = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=10)
    cellphone = forms.CharField(max_length=15)
    birthday = forms.DateField()
    avatar = forms.CharField(max_length=4000)
    date_start = forms.DateField()
    date_end = forms.DateField()
    shift = forms.CharField(max_length=15)
    position = forms.IntegerField()