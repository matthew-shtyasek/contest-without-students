from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if 'is_staff' in extra_fields:
            del extra_fields['is_staff']
        if 'is_superuser' in extra_fields:
            del extra_fields['is_superuser']

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    last_login = None
    is_staff = None
    is_active = True
    is_superuser = None

    objects = CustomUserManager()

    class Meta:
        managed = False
        db_table = 'user'

    USERNAME_FIELD = 'email'
