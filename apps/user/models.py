import environ
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
env = environ.Env()


class UserManager(BaseUserManager):
    def create_user(
            self,
            username,
            email,
            password,
            is_admin=False,
            is_staff=False,
            is_active=True,
            is_superuser=False,
    ):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have email")
        if not password:
            raise ValueError("User must have password")
        user = self.model(username=username)
        user.set_password(password)
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save(using=self.db)

        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError("User must have username")
        if not password:
            raise ValueError("User must have password")
        user = self.create_user(username=username, password=password, email=env("DJANGO_SUPERUSER_EMAIL"))
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self.db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
