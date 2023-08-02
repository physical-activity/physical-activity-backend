import os

import django
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.urls import reverse
from djoser.utils import encode_uid
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'physact.settings')
django.setup()


User = get_user_model()


class UserAPITestCase(APITestCase):

    @staticmethod
    def login_user(client: APIClient, user: User) -> None:
        """ Aутентифицирует пользователя."""

        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    @staticmethod
    def get_registered_user(email: str = 'tests@example.com') -> User:
        """Возвращает пользователя по его email."""

        return User.objects.get(email=email)

    @staticmethod
    def get_error_message(name: str) -> str:
        """Возвращает сообщение с ошибкой."""

        message = {
            'token': 'Invalid token for given user.',
            'field': 'This field may not be blank.',
        }

        return message.get(name)

    def setUp(self) -> None:
        """Создает тестового пользователя перед каждым тестом."""

        self.path = '/api/v1/auth/'
        user = User.objects.create_user(
            first_name='test_user',
            email='tests@example.com',
            password='test_password',
        )
        user.save()

    def test_user_registration_post_success(self) -> None:
        """Тестирует создание пользователя с корректными данными."""

        data = {
            'password': 'Change_Me',
            'email': 'tests@mail.ru',
            'first_name': 'Test',
        }

        self.assertFalse(
            User.objects.filter(
                email=data.get('email')
            ).exists()
        )

        response = self.client.post(
            reverse('api:user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = self.get_registered_user(data.get('email'))

        self.assertTrue(
            User.objects.filter(
                email=data.get('email')
            ).exists()
        )
        self.assertFalse(user.is_active)

    def test_user_registration_post_error(self) -> None:
        """Тестирует создание пользователя с дублирующими
        и некорректными данными."""

        user = self.get_registered_user()
        self.assertTrue(
            User.objects.filter(
                email=user.email
            ).exists()
        )
        user_count = User.objects.count()

        data = {
            'password': 'test_pass',
            'email': 'tests@example.com',
            'first_name': 'test_password',
        }

        response = self.client.post(
            reverse('api:user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count, User.objects.count())

        data['email'] = ''

        response = self.client.post(
            reverse('api:user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count, User.objects.count())

    def test_user_activation_success(self) -> None:
        """Тестирует активацию аккаунта пользователя с корректными данными."""

        user = self.get_registered_user()
        user.is_active = False
        user.save()

        data = {
            'uid': encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
        }

        response = self.client.post(
            reverse(
                'api:activate',
                kwargs=data
            ),
            data,
            format='json'
        )

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        updated_user = User.objects.get(pk=user.id)

        self.assertTrue(updated_user.is_active)

    def test_user_activation_error(self) -> None:
        """Тестирует активацию аккаунта пользователя с некорректным токеном."""

        user = self.get_registered_user()
        user.is_active = False
        user.save()

        data = {
            'uid': encode_uid(user.pk),
            'token': f'{default_token_generator.make_token(user)}invalid',
        }

        response = self.client.post(
            reverse(
                'api:activate',
                kwargs=data
            ),
            data,
            format='json'
        )

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys()), ['token'])
        self.assertEqual(
            response.data.get('token')[0],
            self.get_error_message('token'),
        )

        updated_user = self.get_registered_user()

        self.assertFalse(updated_user.is_active)

    def test_getting_token_success(self) -> None:
        """Тестирует получения токена для аутенфикации
        с корректными данными."""

        data_registered_user = {
            'password': 'test_password',
            'email': 'tests@example.com',
        }

        response = self.client.post(
            f'{self.path}token/login',
            data_registered_user,
            format='json',
        )

        user = self.get_registered_user()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('auth_token'), user.auth_token.key)

    def test_getting_token_error(self) -> None:
        """Тестирует получения токена для аутенфикации
        с некорректными данными."""

        data_registered_user = {
            'password': 'test_password_invalid',
            'email': 'tests@example.com',
        }

        response = self.client.post(
            f'{self.path}token/login',
            data_registered_user,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_token_success(self) -> None:
        """Тестирует удаление токена для аутенфикации
        с корректными данными."""

        client = APIClient()
        user = self.get_registered_user()

        self.login_user(client, user)

        response = client.post(
            f'{self.path}token/logout',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_destroy_token_unauthorized(self) -> None:
        """Тестирует удаление токена для аутенфикации
        с некорректными данными."""

        response = self.client.post(
            f'{self.path}token/logout',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_reset_password_success(self) -> None:
        """Тестирует отправление письма с
        ссылкой для изменения пароля."""

        user = self.get_registered_user()

        data = {'email': user.email}

        response = self.client.post(
            reverse('api:reset_password'),
            data,
            format='json',
        )

        request = response.wsgi_request
        site = get_current_site(request)

        self.assertIn(site.domain, mail.outbox[0].body)
        self.assertIn(site.name, mail.outbox[0].body)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_account_success(self) -> None:
        """Тестирует получения данных пользователя,
        от авторизованного пользователя."""

        client = APIClient()
        user = self.get_registered_user()

        self.login_user(client, user)

        response = client.get(
            reverse('api:account'),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), user.id)

    def test_get_account_unauthorized(self) -> None:
        """Тестирует попытку получения данных пользователя,
        от неавторизованного пользователя."""

        response = self.client.get(
            reverse('api:account'),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_account_success(self) -> None:
        """Тестирует изменения данных пользователя,
        от авторизованного пользователя."""

        client = APIClient()
        user = self.get_registered_user()

        data = {
            'email': 'test_reset@example.com'
        }

        self.login_user(client, user)

        response = client.patch(
            reverse('api:account'),
            data,
            format='json',
        )

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), data['email'])

    def test_patch_account_invalid_data(self) -> None:
        """Тестирует попытку изменения данных пользователя,
        от авторизованного пользователя с некорретными данными."""

        client = APIClient()
        user = self.get_registered_user()

        data = {
            'email': ''
        }

        self.login_user(client, user)

        response = client.patch(
            reverse('api:account'),
            data,
            format='json',
        )

        user.refresh_from_db()

        self.assertContains(
            response,
            text=self.get_error_message('field'),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_patch_account_unauthorized(self) -> None:
        """Тестирует попытку изменения данных пользователя,
        от неавторизованного пользователя."""

        data = {
            'email': 'tests@example.com'
        }

        response = self.client.patch(
            reverse('api:account'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
