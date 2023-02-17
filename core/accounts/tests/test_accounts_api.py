import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = CustomUser.objects.create(
        username="testuser", password="a/123456", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestAccountsAPI:
    """class for testing accounts API."""

    def test_create_user_valid_data_response_201(self, api_client):
        url = reverse("accounts:accounts-api:registration")
        data = {
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "a/123456",
            "password1": "a/123456",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_user_invalid_data_response_400(self, api_client):
        url = reverse("accounts:accounts-api:registration")
        data = {
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "a/123456",
            "password1": "a/12345",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_token_login_response_200(self, api_client, common_user):
        user = common_user
        token = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="token " + str(token[0]))
        url = reverse("todo:todo-api:tasks")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_token_logout_responste_401(self, api_client, common_user):
        user = common_user
        token = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION="token " + str(token[0]))
        url = reverse("todo:todo-api:tasks")
        response = api_client.get(url)
        assert response.status_code == 200
        api_client.credentials()
        response = api_client.get(url)
        assert response.status_code == 401

    def test_jwt_login_response_200(self, api_client, common_user):
        user = common_user
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("todo:todo-api:tasks")
        response = api_client.get(url)
        assert response.status_code == 200
