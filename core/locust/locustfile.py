from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/api/v1/jwt/create/",
            data={
                "username": "admin",
                "password": "123"
            }
        ).json()
        self.client.headers = {"Authorization": f'Bearer {response.get("access", None)}'}


    @task()
    def tasks_list(self):
        self.client.get("todo/api/v1/tasks")
