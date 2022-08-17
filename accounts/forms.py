from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Customer


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "phone")


class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length = 200)

class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "email", "phone")


