import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser


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
class TestTaskAPI:
    """class for testing tasks API."""

    def test_list_tasks_response_401_unauthorized_user(self, api_client):
        url = reverse("todo:todo-api:tasks")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_list_tasks_response_200_logged_in_user(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_201(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_retrieve_task_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        pk = response.data.get("id")
        url = reverse("todo:todo-api:task-detail", kwargs={"pk": pk})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_put_task_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        pk = response.data.get("id")
        url = reverse("todo:todo-api:task-detail", kwargs={"pk": pk})
        data = {"title": "test_task_edited", "completed": True}
        response = api_client.put(url, data)
        assert response.status_code == 200
        assert response.data.get("title") == "test_task_edited"
        assert response.data.get("completed") == True

    def test_patch_task_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        pk = response.data.get("id")
        url = reverse("todo:todo-api:task-detail", kwargs={"pk": pk})
        data = {"completed": True}
        response = api_client.patch(url, data)
        assert response.status_code == 200
        assert response.data.get("completed") == True

    def test_delete_task_response_204(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("todo:todo-api:tasks")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        pk = response.data.get("id")
        url = reverse("todo:todo-api:task-detail", kwargs={"pk": pk})
        response = api_client.delete(url)
        assert response.status_code == 204
