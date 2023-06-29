from locust import HttpUser, task, between, FastHttpUser


class ProjectPerfTest(FastHttpUser):
    wait_time = between(1, 2)

    @task
    def access_index(self):
        self.client.get("/")

    @task
    def access_dashboard(self):
        self.client.get("/dashboard")

    @task
    def logged_in(self):
        self.client.post("/showSummary", data=dict(email="john@simplylift.co"))
        self.client.get("/dashboard")

    @task
    def book_comp(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
        self.client.get("/dashboard")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "3",
            },
        )
        self.client.get("/dashboard")
