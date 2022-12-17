from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def home(self):
        self.client.get("/")
    @task
    def login(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def display_points(self):
        self.client.get('/pointsBoard')
    
    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
           "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": 2
        })

    @task
    def get_book(self):
        self.client.get("book/Spring Festival/Simply Lift")

    @task
    def logout(self):
        self.client.get("/logout")