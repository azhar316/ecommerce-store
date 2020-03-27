from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have password')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, staff=True, admin=True, is_superuser=True)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password, staff=True)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    full_name = models. CharField(max_length=250, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_email(self):
        return self.email

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # override functions of PermissionMixin to enable staff users permission to perform
    # all the admin tasks
    def has_perm(self, perm, obj=None):
        return self.staff

    def has_perms(self, perm_list, obj=None):
        return self.staff

    def has_module_perms(self, app_label):
        return self.staff
