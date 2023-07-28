from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from users.models import CustomUser
from .serializers import UserSerializer  # UserCreateSerializer


@api_view(['GET'])
def users_list(request):
    """
    Временная история.
    """
    queryset = CustomUser.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
def users_detail(request, pk):
    """
    Представление пользователя для ЛК.
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
        activation_link = f"http://PHYSACT.COM/auth/activation/" \
                          f"{user.id}/{token}/"
        subject = 'Account Activation'
        message = f"To activate your account, please follow this link:" \
                  f" {activation_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
          
    queryset = CustomUser.objects.get(id=pk)
    if request.method == 'PATCH':
        serializer = UserSerializer(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(queryset, partial=True)
    return Response(serializer.data)