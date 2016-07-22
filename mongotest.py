from locust import Locust, TaskSet, task, HttpLocust
import random
from pymongo import MongoClient

mongocl = MongoClient('85.255.197.93', 27019)
db = mongocl.get_database('test0')


class MongoCluster(TaskSet):

    @task
    def add_record(self):
        with self.client.get("/", catch_response=True) as response:
            try:
                db.test.insert_one({'title': 'test_%s' % random.random()})
                response.success()
            except Exception as e:
                response.failure(e)
        # print (res)


class WebsiteUser(HttpLocust):
    task_set = MongoCluster
    min_wait = 5
    max_wait = 20
