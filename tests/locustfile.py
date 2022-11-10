from locust import HttpUser, between, task
from test_utils import generate_query, get_n_docs


class LoadTestUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def start_search(self):
        query = generate_query()
        data = {
            "query": query,
            "index": "stackoverflow_tensorflow_use",
            "n_docs": get_n_docs(),
            "distance": "Cosine similarity",
        }
        self.client.post("find", json=data)
