from django.shortcuts import render, redirect, reverse, get_object_or_404
from accounts.models import Profile
from todos.models import Todo
from django.contrib.auth.decorators import login_required
from todos.forms import TodoForm


@login_required
def home(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.is_approved:
        if profile.is_admin:
            unapproved_users = Profile.objects.filter(domain=profile.domain,
                                                     is_approved=False)
            pending_todos = Todo.objects.filter(is_completed=False,
                                                is_active=True,
                                                assigned_to__domain=profile.domain)
            completed_todos = Todo.objects.filter(is_completed=True,
                                                  is_active=True,
                                                  assigned_to__domain=profile.domain)

        else:
            unapproved_users = []
            pending_todos = Todo.objects.filter(assigned_to=profile,
                                                is_completed=False,
                                                is_active=True)
            completed_todos = Todo.objects.filter(assigned_to=profile,
                                                  is_completed=True,
                                                  is_active=True)

        created_todos = Todo.objects.filter(assigned_by=profile,
                                            is_active=True)

        return render(request, 'todos/home.html',
                      {'unapproved_users': unapproved_users,
                       'profile': profile,
                       'completed_todos': completed_todos,
                       'pending_todos': pending_todos,
                       'created_todos': created_todos})
    else:
        return render(request, 'accounts/unapproved_user.html')


@login_required
def add_todo(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = TodoForm(profile, request.POST)
        if form.is_valid():
            todo_form = form.save(commit=False)
            todo_form.assigned_by = profile
            todo_form.profile = profile
            todo_form.save()
            return redirect(reverse('todos:home'))

    else:
        # Overiding forms init instead of the below code:
        # domain_members = MyUser.objects.filter(domain=my_user.domain)
        # TodoForm.base_fields['assigned_to'] = forms.ModelChoiceField(queryset=domain_members)
        form = TodoForm(profile)

    return render(request, 'todos/add_todo.html',
                  {'form': form, 'profile': profile})


@login_required
def complete_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_id)
        todo.is_completed = True
        todo.save()
        return redirect(reverse('todos:home'))


@login_required
def delete_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_id)
        todo.is_active = False
        todo.save()
        return redirect(reverse('todos:home'))


@login_required
def edit_todo(request, todo_id):
    profile = get_object_or_404(Profile, user=request.user)
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        form = TodoForm(profile, request.POST, instance=todo)
        if form.is_valid():
            todo_form = form.save(commit=False)
            todo_form.assigned_by = profile
            todo_form.profile = profile
            todo_form.save()
            return redirect(reverse('todos:home'))

    else:
        form = TodoForm(profile=profile, instance=todo)

        return render(request, 'todos/edit_todo.html', {'form': form})
