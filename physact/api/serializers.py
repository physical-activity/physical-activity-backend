from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import CustomUser

User = get_user_model()


class UserSerializer(UserSerializer):
    """
    User Serializer.
    """
    image = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email',
                  'first_name', 'last_name', 'phone', 'image',)


class UserCreateSerializer(UserCreateSerializer):
    """
    New User Create Serializer.
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'first_name', 'password',)
