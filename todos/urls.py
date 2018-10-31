from django.urls import path
from todos.views import (
    home, add_todo, complete_todo,
    delete_todo, edit_todo, history
)

app_name = 'todos'

urlpatterns = [
    path('', home, name='home'),
    path('todo/add', add_todo, name='add'),
    path('todo/<int:todo_id>/complete', complete_todo, name='complete'),
    path('todo/<int:todo_id>/delete', delete_todo, name='delete'),
    path('todo/<int:todo_id>/edit', edit_todo, name='edit'),
    path('todo/history/', history, name='history')
]
