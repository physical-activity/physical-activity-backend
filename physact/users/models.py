from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """
    User model.
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=settings.USER_FIELDS_LIMIT
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=settings.USER_FIELDS_LIMIT
    )
    email = models.EmailField(
        max_length=settings.USER_FIELDS_LIMIT,
        verbose_name='email',
        unique=True
    )
    phone = models.PhoneNumberField(
        verbose_name='Phone Number',
        unique=True, null=False, blank=False
    )
    photo = models.ImageField(
        upload_to='users/photo/',
        verbose_name='Profile Picture'
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
