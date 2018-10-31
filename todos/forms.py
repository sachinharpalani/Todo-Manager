from django import forms
from todos.models import Todo
from accounts.models import Profile


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        exclude = ('is_completed', 'is_active', 'assigned_by')

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Profile.objects.filter(
            domain=profile.domain
        )

    def save(self, commit=True):
        todo_form = super(TodoForm, self).save(commit=False)
        todo_form.assigned_by = self.profile
        todo_form.profile = self.profile
        if commit:
            todo_form.save()

        return todo_form
