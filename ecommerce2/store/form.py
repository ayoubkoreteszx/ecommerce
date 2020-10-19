from django import forms

class ContactForm(forms.Form):
    contact_name=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','cols':4}))
    contact_email=forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':5}),required=True)