from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from djoser.views import UserViewSet
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import UserSerializer, UserCreateSerializer


class UsersViewSet(UserViewSet):
    """
    Viewset for managing users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        """
        Get or update the current user's information.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserCreateAPIView(generics.CreateAPIView):
    """
    API view for creating a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user and send an account activation email.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        activation_link = f"http://PHYSACT.COM/auth/activation/{user.id}/{token}/"
        subject = 'Account Activation'
        message = f"To activate your account, please follow this link: {activation_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
