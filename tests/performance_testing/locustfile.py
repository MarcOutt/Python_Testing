from locust import HttpUser, between, task


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("")

    @task(3)
    def showSummary(self):
        email = "john@simplylift.co"
        self.client.post("/showSummary", data={"email": email})

    @task(2)
    def book(self):
        competition = "Winter Festival"
        club = "Simply Lift"
        self.client.get(f"/book/{competition}/{club}")

    @task(1)
    def purchasePlaces(self):
        competition = "Winter Festival"
        club = "Simply Lift"
        places = "2"
        self.client.post("/purchasePlaces", data={"competition": competition, "club": club, "places": places})

    @task
    def display(self):
        self.client.get("/display")
