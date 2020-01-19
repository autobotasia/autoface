import pymongo
import time
from datetime import datetime
import random as rd
from save2DB import AutofacesMongoDB
from faker import Faker

mongo_client_address = "mongodb://localhost:27017/"
database_name = "Autofaces"
collection_name = 'PredictFaces'


autofaces_db = AutofacesMongoDB(mongo_client_address, database_name, collection_name)

fake = Faker()

for i in range(10):
    time.sleep(rd.randint(1, 10))
    face_class = fake.name()
    prob = rd.random()
    data = {
        "time": datetime.now(),
        "face_class": face_class,
        "prob": prob
    }
    autofaces_db.save2db(data)
