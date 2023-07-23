from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import AuthUserViewSet

app_name = 'api.v1'

router = DefaultRouter()
router.register("auth", UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/signup/', UserViewSet.create, name='user_create'),
]
