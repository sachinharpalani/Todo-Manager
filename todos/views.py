from django.shortcuts import render, redirect, reverse, get_object_or_404
from accounts.models import MyUser, Domain
from todos.models import Todo
from django.contrib.auth.decorators import login_required
from todos.forms import TodoForm
from django import forms

# Create your views here.


@login_required
def home(request):
    my_user = get_object_or_404(MyUser, user=request.user)
    if my_user.is_approved:
        if my_user.is_admin:
            unapproved_users = MyUser.objects.filter(domain=my_user.domain, is_approved=False)
            pending_todos = [todo for todo in Todo.objects.filter(is_completed=False, is_active=True)
                             if todo.assigned_to.domain == my_user.domain]
            completed_todos = [todo for todo in Todo.objects.filter(is_completed=True, is_active=True)
                               if todo.assigned_to.domain == my_user.domain]

        else:
            unapproved_users = []
            pending_todos = Todo.objects.filter(assigned_to=my_user, is_completed=False, is_active=True)
            completed_todos = Todo.objects.filter(assigned_to=my_user, is_completed=True, is_active=True)

        created_todos = Todo.objects.filter(assigned_by=my_user, is_active=True)

        return render(request, 'home.html',
                      {'unapproved_users': unapproved_users,
                       'my_user': my_user,
                       'completed_todos': completed_todos,
                       'pending_todos': pending_todos,
                       'created_todos': created_todos})
    else:
        return render(request, 'unapproved_user.html')


@login_required
def add_todo(request):
    my_user = get_object_or_404(MyUser, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_form = form.save(commit=False)
            todo_form.assigned_by = my_user
            todo_form.save()
            return redirect(reverse('todos:home'))

    else:
        domain_members = MyUser.objects.filter(domain=my_user.domain)
        TodoForm.base_fields['assigned_to'] = forms.ModelChoiceField(queryset=domain_members)
        form = TodoForm()

    return render(request, 'add_todo.html', {'form': form})


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
    my_user = get_object_or_404(MyUser, user=request.user)
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo_form = form.save(commit=False)
            todo_form.assigned_by = my_user
            todo_form.save()
            return redirect(reverse('todos:home'))

    else:
        form = TodoForm(instance=todo)

    return render(request, 'edit_todo.html', {'form': form})
