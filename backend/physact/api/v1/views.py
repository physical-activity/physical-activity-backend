from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .serializers import UserCreateSerializer

User = get_user_model()


class AuthUserViewSet(UserViewSet):
    """Use this endpoint to create user."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
