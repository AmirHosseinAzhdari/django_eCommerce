from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import OtpCode, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "mobile_number", "full_name")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError("Passwords dont match!")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='You can change password using <a href="../password/">this form</a>'
    )

    class Meta:
        model = User
        fields = ("email", "mobile_number", "full_name", "password", "last_login")


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    full_name = forms.CharField(
        label="full name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    mobile_number = forms.CharField(
        label="phone number", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cd = super().clean()
        if User.objects.filter(email=cd["email"]).exists():
            self.add_error("email", "This email is already exist")
        if User.objects.filter(mobile_number=cd["mobile_number"]).exists():
            self.add_error("mobile_number", "This mobile number is already exist")


class VerifyOtpForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
