from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from djoser.views import ActivationView, UserViewSet
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[AllowAny],
        url_path='activation',
    )
    def activate(self, request, *args, **kwargs):
        return CustomActivationView.as_view()(
            request._request, *args, **kwargs)


class CustomUserCreateAPIView(generics.CreateAPIView):
    """
    API view for creating a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

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
        activation_link = (
            f"http://PHYSACT.COM/api/{settings.API_VERSION}/"
            f"auth/activation/{user.id}/{token}/"
        )
        subject = 'Account Activation'
        message = (
            f"To activate your account, please follow this link: "
            f"{activation_link}"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomActivationView(ActivationView):
    """"
    View to enable activation in for custom UserViewSet
    """
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class LogoutView(APIView):
    """
    API view to enable custom logout
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)