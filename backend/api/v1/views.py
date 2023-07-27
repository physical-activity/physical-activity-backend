from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import UserSerializer


@api_view(['GET'])
def users_list(request):
    """
    Users List View.
    """
    queryset = CustomUser.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
def users_detail(request, pk):
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
