from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """
    New User Create Serializer.
    """

    class Meta:
        model = User
        fields = (
            'email', 'password', 'username',
        )
