from django import forms
from accounts.models import Customer
from store.models import Category
from restaurants.models import Restaurant



class NewTableForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name",)

class NewProdutcForm(forms.Form):
    name = forms.CharField(max_length=200)
    price = forms.IntegerField()
    description = forms.CharField(max_length=200)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class UptadeRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"






