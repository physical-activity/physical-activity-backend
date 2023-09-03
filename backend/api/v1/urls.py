from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import TrainingsViewSet, TrainingTypesViewSet, GoogleLogin, VKLogin

router_v1 = DefaultRouter()
router_v1.register('trainings', TrainingsViewSet)
router_v1.register(
    'training_types', TrainingTypesViewSet, basename='training_types'
)

urlpatterns = [
    path(
        'auth/signup/',
        UserViewSet.as_view({'post': 'create'}), name='user_create'
    ),
    path(
        'auth/activation/<str:uid>/<str:token>/',
        UserViewSet.as_view({'post': 'activation'}), name='activate'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/vk/', VKLogin.as_view(), name='vk_login'),
    path(
        'auth/reset_password/',
        UserViewSet.as_view({'post': 'reset_password'}),
        name='reset_password'
    ),
    path(
        'auth/set_new_password/<str:uid>/<str:token>/',
        UserViewSet.as_view({'post': 'reset_password_confirm'}),
        name='set_new_password'
    ),
    path(
        'account/',
        UserViewSet.as_view({'get': 'me', 'patch': 'me'}),
        name='account'
    ),

    path('', include(router_v1.urls)),
]
