from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    User model.
    """

    USERNAME_FIELD = 'email'

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=settings.USER_FIELDS_LIMIT
    )
    last_name = models.CharField(
        max_length=settings.USER_FIELDS_LIMIT,
        verbose_name='Last Name',
    )
    email = models.EmailField(
        max_length=settings.USER_FIELDS_LIMIT,
        verbose_name='email',
        unique=True
    )
    photo = models.ImageField(
        upload_to='users/photo/',
        verbose_name='Profile Picture'
    )
    phone = models.CharField(
        max_length=settings.USER_FIELDS_LIMIT,
        verbose_name='Phone Number',
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
