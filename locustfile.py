from locust import HttpUser, task, between
from faker import Faker
import datetime
import random

"""
[endpoints]
- es: elasticsearch-dsl
- async-lock-es: elasticsearch-dsl + async-lock
- mongo: odmantic
- es-py: elasticsearch-py

GETについてはidや返り値がそれぞれ微妙に異なるので別々に用意
"""


fake = Faker()

"""
# POST load_test
class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def create_item(self):
        data = {
            "name": fake.name(),
            "price": fake.random_int(min=1, max=1000),
            "description": fake.sentence(),
            "model_config": {
                "from_attributes": True
            },
            "tax": fake.random_int(min=0, max=50),
            "updated_at": datetime.datetime.now().isoformat()
        }
        self.client.post("/item/async-lock-es", json=data)
"""



# ODMantic GET load_test
class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)
    mongo_ids = []

    def on_start(self):
        # on_start is called when a Locust start before any task is scheduled
        if not UserBehavior.mongo_ids:  
            response = self.client.get("/item/mongo")
            items = response.json()
            UserBehavior.mongo_ids = [item['id'] for item in items]

    @task
    def get_random_mongo_item(self):
        item_id = random.choice(UserBehavior.mongo_ids)
        self.client.get(f"/item/mongo/{item_id}")



"""
# Elasticsearch-dsl GET load_test
class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)
    es_ids = []

    def on_start(self):
        if not UserBehavior.es_ids:
            response = self.client.get("/item/async-lock-es")
            items = response.json()['hits']['hits']
            UserBehavior.es_ids = [item['_id'] for item in items]

    @task
    def get_random_es_item(self):
        item_id = random.choice(UserBehavior.es_ids)
        self.client.get(f"/item/async-lock-es/{item_id}")
"""

"""
# Elasticsearch-py GET load_test
class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)
    es_ids = []

    def on_start(self):
        if not UserBehavior.es_ids:
            response = self.client.get("/item/es-py")
            items = response.json()
            UserBehavior.es_ids = [item['_id'] for item in items]
        

    @task
    def get_random_es_item(self):
        item_id = random.choice(UserBehavior.es_ids)
        self.client.get(f"/item/es-py/{item_id}")
"""