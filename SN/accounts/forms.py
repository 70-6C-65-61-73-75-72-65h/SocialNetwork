from django import forms
from pagedown.widgets import PagedownWidget
from .models import Profile

class ProfileForm(forms.ModelForm):
    """ called only for update """
    bio = forms.CharField(widget=PagedownWidget(), required=False)
    birth_date = forms.CharField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "birth_date",
            "image",
        ]

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
        