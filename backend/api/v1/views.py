from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from trainings.models import Training, TrainingType
from users.models import CustomUser
from .filters import TrainingsFilter
from .paginators import CustomPageNumberPagination
from .permissions import AuthorOnly
from .serializers import (
    TrainingSerialaizer, TrainingTypeSerializer, UserSerializer,
)


@api_view(['GET'])
def users_list(_):
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
    permission_classes = (AuthorOnly, )
    serializer_class = TrainingSerialaizer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TrainingsFilter

    def get_queryset(self):
        user = self.request.user
        queryset = user.trainings.all()
        return queryset


@api_view(['GET'])
def training_types_list(_):
    """
    Training Types List View.
    """
    queryset = TrainingType.objects.all()
    serializer = TrainingTypeSerializer(queryset, many=True)
    return Response(serializer.data)
