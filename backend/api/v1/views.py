from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trainings.models import Training
from users.models import CustomUser
from .serializers import TrainingSerialaizer, UserSerializer


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


class TrainingsViewSet(viewsets.ModelViewSet):
    """
    Trainings View.
    """
    queryset = Training.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TrainingSerialaizer

    def get_queryset(self):
        user = self.request.user
        queryset = user.trainings.all()
        return queryset
