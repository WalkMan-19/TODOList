import pytest
from django.urls import reverse
from rest_framework import status

from core.serializers import LoginUserSerializer, ProfileSerializer


@pytest.mark.django_db
class TestSignUp:
    url = reverse('signup-view')

    def test_signup_success(self, api_client, faker):
        password = faker.password()
        username = faker.user_name()

        user = {
            "username": username,
            "password": password,
            "password_repeat": password,
        }
        response = api_client.post(self.url, data=user)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == username

    def test_signup_failed(self, api_client, faker):
        username = faker.user_name()
        password = faker.password()
        password_repeat = faker.password()
        user = {
            "username": username,
            "password": password,
            "password_repeat": password_repeat,
        }
        response = api_client.post(self.url, data=user)
        assert password != password_repeat
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password_repeat': ['Passwords must match']}

    def test_password_validation(self, api_client, faker):
        username = faker.user_name()
        password = faker.password(length=4)
        user = {
            "username": username,
            "password": password,
            "password_repeat": password
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password': ['This password is too short. It must contain at least 8 '
                                                'characters.'],
                                   'password_repeat': ['This password is too short. It must contain at least 8 '
                                                       'characters.']}

        password = '12345678'
        user = {
            'username': username,
            'password': password,
            'password_repeat': password
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password': ['This password is too common.',
                                                'This password is entirely numeric.'],
                                   'password_repeat': ['This password is too common.',
                                                       'This password is entirely numeric.']}


@pytest.mark.django_db
class TestLogin:
    url = reverse('login-view')

    def test_login_success(self, api_client, user_factory, faker):
        password = faker.password()
        user = user_factory.create(password=password)
        response = api_client.post(self.url, data={'username': user.username,
                                                   'password': password,
                                                   })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == LoginUserSerializer(user).data

    def test_login_failed(self, api_client, user_factory):
        user = user_factory.build()
        response = api_client.post(self.url, data={'username': user.username,
                                                   'password': user.password,
                                                   })
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestProfile:
    url = reverse('profile-view')

    def test_get_profile_success(self, api_client, login_user, current_user):
        response = login_user.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == ProfileSerializer(current_user).data

    def test_get_profile_failed(self, api_client):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_edit_profile_success(self, login_user, current_user, faker):
        username = current_user.username
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()

        response = login_user.put(self.url, data={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })
        expected_data = {
            'id': current_user.id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_data

    def test_partial_edit_profile_success(self, login_user, current_user, faker):
        last_name = faker.last_name()

        response = login_user.patch(self.url, data={
            'last_name': last_name,
        })
        expected_data = {
            'id': current_user.id,
            'username': current_user.username,
            'first_name': current_user.first_name,
            'last_name': last_name,
            'email': current_user.email,
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_data

    def test_delete_profile_success(self, login_user, current_user):
        response = login_user.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUpdatePassword:
    url = reverse('update_password-view')

    def test_update_user_password_success(self, api_client, faker, user_factory):
        password = faker.password()
        new_password = faker.password()
        user = user_factory.create(password=password)

        api_client.force_login(user)
        response = api_client.put(self.url, data={
            'old_password': password,
            'new_password': new_password,
        })
        assert response.status_code == status.HTTP_200_OK

    def test_update_user_password_failed(self, api_client, faker, user_factory):
        password = faker.password()
        new_password = faker.password(length=4)
        user = user_factory.create(password=password)

        api_client.force_login(user)
        response = api_client.put(self.url, data={
            'old_password': password,
            'new_password': new_password,
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'new_password': ['This password is too short. It must contain at least 8 characters.']
        }
