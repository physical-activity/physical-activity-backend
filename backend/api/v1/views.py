from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from trainings.models import Training, TrainingType

from .filters import TrainingsFilter
from .paginators import CustomPageNumberPagination
from .permissions import AuthorOnly
from .serializers import TrainingSerialaizer, TrainingTypeSerializer, \
    GoogleLoginSerializer, VKLoginSerializer


class GoogleLogin(SocialLoginView):
    serializer_class = GoogleLoginSerializer


class VKLogin(SocialLoginView):
    serializer_class = VKLoginSerializer


class TrainingsViewSet(viewsets.ModelViewSet):
    """Trainings View."""

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


class TrainingTypesViewSet(viewsets.ViewSet):
    """Training Types List View."""

    def list(self, _):
        queryset = TrainingType.objects.all()
        serializer = TrainingTypeSerializer(queryset, many=True)
        return Response(serializer.data)
