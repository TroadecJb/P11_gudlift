from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task(6)
    def index(self):
        self.client.get("/")
