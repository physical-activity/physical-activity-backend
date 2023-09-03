from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=settings.USER_FIELDS_LIMIT
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=settings.USER_FIELDS_LIMIT,
        blank=True
    )
    email = models.EmailField(
        max_length=settings.USER_FIELDS_LIMIT,
        verbose_name='email',
        unique=True
    )
    phone = PhoneNumberField(
        verbose_name='Phone Number',
        unique=True, null=True, blank=True
    )
    photo = models.ImageField(
        upload_to='users/photo/',
        verbose_name='Profile Picture',
        blank=True
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        ordering = ('id', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
