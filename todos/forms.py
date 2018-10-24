from django import forms
from todos.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        exclude = ('is_completed', 'is_active', 'assigned_by')
