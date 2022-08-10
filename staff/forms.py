from django import forms
from accounts.models import Customer


class NewTableForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name",)





