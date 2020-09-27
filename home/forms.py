from django import forms



class RegisterForm(forms.Form):
    name = forms.CharField(max_length=140)
    email = forms.EmailField(required=False)
    soc_url = forms.CharField(max_length=140)
    category = forms.CharField(max_length=140)
