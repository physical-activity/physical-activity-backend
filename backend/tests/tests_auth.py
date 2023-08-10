import os

import django
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
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
        """Authenticates the user."""

        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    @staticmethod
    def get_registered_user(email: str = 'tests@example.com') -> User:
        """Returns the user by his email."""

        return User.objects.get(email=email)

    def setUp(self) -> None:
        """Creates a test user before each test."""

        self.path = '/api/v1/auth/'
        user = User.objects.create_user(
            first_name='test_user',
            email='tests@example.com',
            password='test_password',
        )
        user.save()

    def test_user_registration_post_success(self) -> None:
        """Tests the creation of a user with correct data."""

        data = {
            'password': 'Change_Me',
            'email': 'tests@mail.ru',
            'first_name': 'Test',
        }

        self.assertFalse(User.objects.filter(email=data['email']).exists())

        response = self.client.post(
            reverse('user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = self.get_registered_user(data['email'])

        self.assertTrue(User.objects.filter(email=data['email']).exists())
        self.assertFalse(user.is_active)

    def test_user_registration_post_error(self) -> None:
        """Creation of a user with duplicate and incorrect data."""

        user = self.get_registered_user()

        self.assertTrue(User.objects.filter(email=user.email).exists())

        user_count = User.objects.count()

        data = {
            'password': 'test_pass',
            'email': user.email,
            'first_name': 'test_password',
        }

        response = self.client.post(
            reverse('user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count, User.objects.count())

        data['email'] = ''

        response = self.client.post(
            reverse('user_create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count, User.objects.count())

    def test_user_activation_success(self) -> None:
        """Activation of the user's account with the correct data."""

        user = self.get_registered_user()
        user.is_active = False
        user.save()

        data = {
            'uid': encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
        }

        response = self.client.post(
            reverse('activate', kwargs=data),
            data,
            format='json',
        )

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        updated_user = User.objects.get(pk=user.id)

        self.assertTrue(updated_user.is_active)

    def test_user_activation_error(self) -> None:
        """Activation of a user's account with an incorrect token."""

        user = self.get_registered_user()
        user.is_active = False
        user.save()

        data = {
            'uid': encode_uid(user.pk),
            'token': f'{default_token_generator.make_token(user)}invalid',
        }

        response = self.client.post(
            reverse('activate', kwargs=data),
            data,
            format='json',
        )

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys()), ['token'])

        updated_user = self.get_registered_user()

        self.assertFalse(updated_user.is_active)

    def test_getting_token_success(self) -> None:
        """Request a token for authentication with correct data."""

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
        """Request a token for authentication with incorrect data."""

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
        """Removing an authentication token with correct data."""

        user = self.get_registered_user()
        client = APIClient()
        self.login_user(client, user)

        response = client.post(f'{self.path}token/logout', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_destroy_token_unauthorized(self) -> None:
        """Removal of the token for authentication with incorrect data."""

        response = self.client.post(f'{self.path}token/logout', format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account_success(self) -> None:
        """Requesting user data, from an authorized user."""

        user = self.get_registered_user()
        client = APIClient()
        self.login_user(client, user)

        response = client.get(reverse('account'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), user.id)

    def test_get_account_unauthorized(self) -> None:
        """Requesting user data, from an unauthorized user."""

        response = self.client.get(reverse('account'), format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_account_success(self) -> None:
        """Request to change user data, from an authorized user."""

        user = self.get_registered_user()
        client = APIClient()
        self.login_user(client, user)

        data = {'email': 'test_reset@example.com'}

        response = client.patch(reverse('account'), data, format='json')

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])

    def test_patch_account_invalid_data(self) -> None:
        """Request to change user data,
        from an authorized user with incorrect data."""

        client = APIClient()
        user = self.get_registered_user()

        data = {'email': ''}

        self.login_user(client, user)

        response = client.patch(reverse('account'), data, format='json')

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_account_unauthorized(self) -> None:
        """Request to change user data, from an unauthorized user."""

        data = {'email': 'tests@example.com'}

        response = self.client.patch(
            reverse('account'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
