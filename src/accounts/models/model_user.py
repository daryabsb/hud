from django.db import models
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from src.accounts.managers import UserManager
# from src.configurations.models import SecurityKey
from src.core.modules import upload_image_file_path
from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin,_user_has_perm)

def _user_has_model_op_perms(user, app_label, model_name):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_model_op_perms'):
            continue
        try:
            if backend.has_model_op_perms(user, app_label, model_name):
                return True
        except PermissionDenied:
            return False

    return False

class User(PermissionsMixin, AbstractBaseUser):
    # Custom user model supports email instead of username
    access_level = models.OneToOneField(
        "SecurityKey", on_delete=models.CASCADE, null=True,
        blank=True, related_name="access_level"
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, default='user.png',
        upload_to=upload_image_file_path)
    pin = models.SmallIntegerField(default=1699)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def has_model_op_perms(self, app_label, model_name):
        """
        Returns True if the user has any operation permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        if self.is_active:
            if self.is_superuser:
                return True
        return _user_has_model_op_perms(self, app_label, model_name)
    
    def has_perm(self, perm, obj=None):
        if self.is_active:
            if self.is_superuser:
                return check_perms_available(perm)
        return _user_has_perm(self, perm, obj)
    
def check_perms_available(perm):
    from src.core.management import maintain_perms_cache
    _cached_perms = maintain_perms_cache(op='fetch')
    if _cached_perms is None:
        _cached_perms = maintain_perms_cache(op='update')
        assert _cached_perms, 'Please ensure `Memcached`(or other cache back-end) is running!!1'
        if perm in _cached_perms:
            return True
        return False