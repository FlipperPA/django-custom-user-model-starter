from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Manager for the User model. Custom methods for creating users and superusers, which
    tie into all parts of Django, including manage.py.
    """

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Pleiades users. Uses 'email' as username.
    """
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True, db_index=True
    )
    full_name = models.CharField(max_length=255, blank=True)
    nick_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.nick_name

    def __str__(self):
        return f"{self.email} ({self.full_name})"
