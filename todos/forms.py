from django import forms
from todos.models import Todo
from accounts.models import Profile


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        exclude = ('is_completed', 'is_active', 'assigned_by')

    def __init__(self, profile, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Profile.objects.filter(domain=profile.domain)
