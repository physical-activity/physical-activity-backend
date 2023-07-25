from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, CustomUserCreateAPIView, LogoutView

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'auth/signup/',
        CustomUserCreateAPIView.as_view(), name='user-create'
    ),
    path(
        'auth/token/login/',
        TokenObtainPairView.as_view(),
        name='user-login'
    ),
    path(
        'auth/activation/<str:uid>/<str:token>/',
        UserViewSet.as_view({'post': 'activate'}),
        name='activate'
    ),
    path(
        'auth/reset-password/',
        UserViewSet.as_view({'post': 'reset_password'}),
        name='reset_password'
    ),
    path(
        'auth/set_new_password/<str:uid>/<str:token>/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='auth_change_password'
    ),
    path(
        'logout/',
        LogoutView.as_view(), name='auth_logout'
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
