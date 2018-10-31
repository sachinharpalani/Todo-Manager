from django.db import models
from django.contrib.auth.models import User


class Domain(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
