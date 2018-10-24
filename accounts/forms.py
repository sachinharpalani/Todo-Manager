from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )
        widgets = {
            # telling Django your field in the mode is a password input
            'password': forms.PasswordInput()
        }
