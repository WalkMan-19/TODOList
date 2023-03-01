import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def current_user(user):
    return user


@pytest.fixture
@pytest.mark.django_db
def login_user(api_client, current_user):
    api_client.force_login(current_user)
    return api_client
