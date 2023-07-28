from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import UserSerializer


class UsersViewSet(UserViewSet):
    """
    Users List View.
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
    User View.
    """
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
