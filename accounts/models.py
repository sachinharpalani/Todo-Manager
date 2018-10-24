from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    @property
    def domain(self):
        domain_name = self.user.email.split('@')[1]
        return domain_name

    def __str__(self):
        return self.user.username


class Team(models.Model):
    domain = models.CharField(max_length=50)
    members = models.ManyToManyField(MyUser)
