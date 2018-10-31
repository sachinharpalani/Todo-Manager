from django.shortcuts import get_object_or_404
from accounts.models import Profile
from functools import wraps
from django.core.exceptions import PermissionDenied


def only_admin(function):

    @wraps(function)
    def wrapper(request, *args, **kwargs):
        admin = get_object_or_404(Profile, user=request.user)
        user_id = kwargs.get('user_id')
        user = get_object_or_404(Profile, pk=user_id)
        if admin.is_admin and admin.domain == user.domain:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper
