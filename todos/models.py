from django.db import models
from accounts.models import Profile

# Create your models here.


class Todo(models.Model):
    content = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(Profile, on_delete=models.PROTECT,
                                    related_name='task_assigned_to')
    assigned_by = models.ForeignKey(Profile, on_delete=models.PROTECT,
                                    related_name='task_assigned_by')
