from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from store.models import Address
from dashboard.models import NurseryManager
from .models import User, UserProfile


class CreateUserForm(UserCreationForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def signup(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        required = ['first_name', 'last_name']


class UpdateAddressForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)').formfield(
        required=False, widget=CountrySelectWidget(attrs={
            'class': 'form-control custom-select my-1 width-90'}))

    class Meta:
        model = Address
        fields = ['city', 'district', 'street_address', 'country']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'biography']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }


class NurseryManagerRegistration(forms.ModelForm):
    class Meta:
        model = NurseryManager
        exclude = ['user']
