from django.contrib import admin
from accounts.models import MyUser, Domain

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Domain)
