from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.forms import RegisterUserForm, LoginUserForm
from TodoManager.settings import LOGIN_REDIRECT_URL
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from accounts.models import MyUser, Team
from django.db import IntegrityError

# Create your views here.


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
                return render(request, 'register.html', {'form': form})

            my_user = MyUser.objects.create(user=user)
            domain_team, is_first_user = Team.objects.get_or_create(domain=my_user.domain)
            if is_first_user:
                my_user.is_admin = True
                my_user.is_approved = True
                my_user.save()
            domain_team.members.add(my_user)
            auth_login(request, user)
            return redirect(LOGIN_REDIRECT_URL)

    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {'form': form})


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
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginUserForm()

        return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('todos:home'))


def approve_account(request):
    if request.method == 'POST':
        print(request.POST.get('user_id'))
        user_id = request.POST.get('user_id')
        my_user = get_object_or_404(MyUser, pk=user_id)
        my_user.is_approved = True
        my_user.save()
        return redirect(reverse('todos:home'))