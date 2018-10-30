from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.forms import RegisterUserForm, LoginUserForm
from TodoManager.settings import LOGIN_REDIRECT_URL, EMAIL_HOST_USER
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout
)
from accounts.models import Profile
from accounts.utils import send_email


def registration(request):
    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(LOGIN_REDIRECT_URL)

    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = LoginUserForm(request.POST)
            if form.is_valid():
                auth_login(request, form.user)
                return redirect(LOGIN_REDIRECT_URL)
        else:
            form = LoginUserForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect(reverse('todos:home'))


def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect(reverse('todos:home'))


def approve_account(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, pk=user_id)
        profile.is_approved = True
        profile.save()
        send_email.delay('Profile Approved',
                         'Your profile has been approved. Please visit our todo app to start managing your tasks',
                         EMAIL_HOST_USER,
                         [profile.user.email])
        return redirect(reverse('todos:home'))
