from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user class."""

    email = models.EmailField(
        max_length=100,
        verbose_name='Email',
        unique=True, blank=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Name',
        blank=False
    )
    surname = models.CharField(
        max_length=150,
        verbose_name='Surname',
        default=None, blank=True, null=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone number',
        default=None, blank=True, null=True
    )
    photo = models.ImageField(
        verbose_name='Photo', upload_to='users/images/',
        default=None, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"
        ordering = ['email']
    
    def __str__(self):
        return self.email[:30]

