from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.forms import RegisterUserForm, LoginUserForm
from TodoManager.settings import LOGIN_REDIRECT_URL
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from accounts.models import MyUser, Domain
from django.db import IntegrityError


def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            try:
                user.save()
            except IntegrityError:
                form.add_error('email', 'Email already exists!')
                return render(request, 'accounts/register.html', {'form': form})

            _domain = user.email.split('@')[1]
            domain_team, is_first_user = Domain.objects.get_or_create(name=_domain)
            my_user = MyUser.objects.create(user=user, domain=domain_team)
            if is_first_user:
                my_user.is_admin = True
                my_user.is_approved = True
                my_user.save()
            auth_login(request, user)
            return redirect(LOGIN_REDIRECT_URL)

    else:
        form = RegisterUserForm()

    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(LOGIN_REDIRECT_URL)
            else:
                form.add_error('password', 'Wrong Email/ Password combination')
                return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginUserForm()

        return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('todos:home'))


def approve_account(request, user_id):
    if request.method == 'POST':
        my_user = get_object_or_404(MyUser, pk=user_id)
        my_user.is_approved = True
        my_user.save()
        return redirect(reverse('todos:home'))
