from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def required_security_level(level, redirect_url='not-authorized'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.access_level.level <= level:
                return view_func(request, *args, **kwargs)
            return redirect(redirect_url)
        return _wrapped_view
    return decorator
