from django.shortcuts import render, redirect, reverse, get_object_or_404
from accounts.models import Profile
from todos.models import Todo
from django.contrib.auth.decorators import login_required
from todos.decorators import approval_required
from todos.forms import TodoForm
from django.db.models import Q


@login_required
@approval_required
def home(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.is_admin:
        q = Q(assigned_to__domain=profile.domain)
        unapproved_users = Profile.objects.filter(
            domain=profile.domain,
            is_approved=False
        )

        completed_count = Todo.objects.filter(
            is_completed=True,
            is_active=True,
            assigned_to__domain=profile.domain
        ).count()

        todos_count = Todo.objects.filter(
            is_active=True,
            assigned_to__domain=profile.domain
        ).count()

        users_count = Profile.objects.filter(
            domain=profile.domain
        ).count()
    else:
        q = Q(assigned_to=profile)
        unapproved_users = completed_count = todos_count = users_count = 0

    pending_todos = Todo.objects.filter(q & Q(
        is_completed=False,
        is_active=True)
    )

    return render(
        request,
        'todos/home.html',
        {
            'unapproved_users': unapproved_users,
            'profile': profile,
            'completed_count': completed_count,
            'pending_todos': pending_todos,
            'todos_count': todos_count,
            'users_count': users_count
        }
    )


@login_required
@approval_required
def add_todo(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.POST:
        form = TodoForm(profile, request.POST)
        if form.is_valid():
            form.save(profile)
            return redirect(reverse('todos:home'))

    else:
        form = TodoForm(profile)

    return render(
        request,
        'todos/add_todo.html',
        {
            'form': form, 'profile': profile
        }
    )


@login_required
@approval_required
def complete_todo(request, todo_id):
    if request.POST:
        todo = get_object_or_404(Todo, id=todo_id)
        todo.is_completed = True
        todo.save()
        return redirect(reverse('todos:home'))


@login_required
@approval_required
def delete_todo(request, todo_id):
    if request.POST:
        todo = get_object_or_404(Todo, id=todo_id)
        todo.is_active = False
        todo.save()
        return redirect(reverse('todos:home'))


@login_required
@approval_required
def edit_todo(request, todo_id):
    profile = get_object_or_404(Profile, user=request.user)
    todo = get_object_or_404(Todo, id=todo_id)
    if request.POST:
        form = TodoForm(profile, request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect(reverse('todos:home'))

    else:
        form = TodoForm(profile=profile, instance=todo)

        return render(request, 'todos/edit_todo.html', {'form': form})


@login_required
@approval_required
def history(request):
    profile = get_object_or_404(Profile, user=request.user)
    todo_type = request.GET.get('todo_type', 'pending')
    q = (
        Q(assigned_to__domain=profile.domain)
        if profile.is_admin
        else Q(assigned_to=profile)
    )
    baseQ = Todo.objects.filter(q)

    if todo_type == 'pending':
        color = 'yellow darken-3'
        q = Q(is_completed=False)

    elif todo_type == 'completed':
        color = 'green'
        q = Q(is_completed=True)

    elif todo_type == 'created':
        color = 'teal'
        q = Q(assigned_by=profile)

    all_todos = baseQ.filter(q & Q(is_active=True))
    return render(
        request,
        'todos/history.html',
        {
            'todos': all_todos,
            'profile': profile,
            'color': color
        }
    )
