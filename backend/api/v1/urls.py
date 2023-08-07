from django.urls import include, path
from djoser.views import UserViewSet

from .views import users_detail, users_list

app_name = 'api'


urlpatterns = [
    path(
        'auth/signup/',
        UserViewSet.as_view({'post': 'create'}), name='user_create'
    ),
    path(
        'auth/activation/<str:uid>/<str:token>/',
        UserViewSet.as_view({'post': 'activation'}), name='activate'
    ),
    path('auth/', include('djoser.urls.authtoken', 'allauth.urls')),
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

    path('users/', users_list),
    path('users/<int:pk>/', users_detail),
]
