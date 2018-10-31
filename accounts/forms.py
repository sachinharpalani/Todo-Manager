from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import Profile, Domain
from accounts.utils import send_email
from TodoManager.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data.get('email')
        is_email_used = User.objects.filter(username=data).exists()
        if is_email_used:
            raise forms.ValidationError("Email already exists!")

        return data

    def save(self):
        user = super(RegisterUserForm, self).save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.save()
        _domain = user.email.split('@')[1]
        domain_team, is_first_user = Domain.objects.get_or_create(name=_domain)
        profile = Profile.objects.create(user=user, domain=domain_team)
        if is_first_user:
            profile.is_admin = True
            profile.is_approved = True
            profile.save()
        else:
            admin = Profile.objects.get(domain=profile.domain, is_admin=True)
            send_email.delay(
                'New Registration',
                '{} has just registered, please approve his profile'.format(
                    profile.user.get_full_name()
                ),
                EMAIL_HOST_USER,
                [admin.user.email]
            )
        return user


class LoginUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        self.user = authenticate(username=email, password=password)
        if self.user is None:
            raise forms.ValidationError('Wrong Email/ Password combination')
