from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import CustomUser


class UserSerializer(UserSerializer):
    """User Serializer"""
    image = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'image',)


class UserCreateSerializer(UserCreateSerializer):
    """New User Create Serializer"""

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password',)
