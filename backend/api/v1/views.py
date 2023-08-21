from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from trainings.models import Training, TrainingType

from .filters import TrainingsFilter
from .paginators import CustomPageNumberPagination
from .permissions import AuthorOnly
from .serializers import TrainingSerialaizer, TrainingTypeSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class VKLogin(SocialLoginView):
    adapter_class = VKOAuth2Adapter
    callback_url = 'https://easyfit.space'
    client_class = OAuth2Client


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
