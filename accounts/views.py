from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.forms import RegisterUserForm, LoginUserForm
from TodoManager.settings import LOGIN_REDIRECT_URL, EMAIL_HOST_USER
from django.contrib.auth import authenticate, \
    login as auth_login, logout as auth_logout
from accounts.models import Profile, Domain
from django.db import IntegrityError
from accounts.utils import send_email


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
                return render(request, 'accounts/register.html',
                              {'form': form})

            _domain = user.email.split('@')[1]
            domain_team, is_first_user = Domain.objects.get_or_create(name=_domain)
            profile = Profile.objects.create(user=user, domain=domain_team)
            if is_first_user:
                profile.is_admin = True
                profile.is_approved = True
                profile.save()
            else:
                admin = Profile.objects.get(domain=profile.domain, is_admin=True)
                print(admin)
                send_email.delay('New Registration', '{} has just registered, please approve his profile'.format(profile.user.get_full_name()), EMAIL_HOST_USER, [admin.user.email])
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
        profile = get_object_or_404(Profile, pk=user_id)
        profile.is_approved = True
        profile.save()
        send_email.delay('Profile Approved', 'Your profile has been approved. Please visit our todo app to start managing your tasks', EMAIL_HOST_USER, [profile.user.email])
        return redirect(reverse('todos:home'))
