import pymongo
import time
from datetime import datetime
import random as rd
from save2DB import AutofacesMongoDB
from faker import Faker
import dbconfig

# MongoDB info
username = dbconfig.DBUSERNAME
password = dbconfig.DBPASSWORD
host = dbconfig.DBHOST
port = dbconfig.DBPORT
database_name = dbconfig.DBNAME
collection_name = dbconfig.COLNAME



autofaces_db = AutofacesMongoDB(username, password, host, port, database_name, collection_name)

def test_save():
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


def show_data():
    collection_ = autofaces_db.client[database_name][collection_name]
    for e in collection_.find().sort('_id',-1):
        print(e)


show_data()
