from functools import wraps
from django.shortcuts import get_object_or_404, render
from accounts.models import Profile


def approval_required(function):

    @wraps(function)
    def wrapper(request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        if profile.is_approved:
            return function(request, *args, **kwargs)
        else:
            return render(request, 'accounts/unapproved_user.html')

    return wrapper
