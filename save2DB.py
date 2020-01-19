import pymongo

class AutofacesMongoDB():

    def __init__(self, username, password, host, port, db = None, col = None):
        '''

        '''
        mongodb_uri = "mongodb://%s:%s@%s:%s"%(user, password, host, port)
        self.host = host
        self.port = port
        print("Connecting to MongoDB...")
        try:
            self.client = pymongo.MongoClient(mongodb_uri)
        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to server: %s" % e)
        print("Mongo connected.")
        print("MongoDB host: %s" % self.host)
        print("MongoDB port: %s" % self.port)
        self.db = db
        self.collection = col
        print("Default database: %s" % self.db)
        print("Default collection: %s" % self.collection)


    def dbinfo(self):
        print("MongoDB host: %s" % self.host)
        print("MongoDB port: %s" % self.port)
        print("Default database: %s" % self.db)
        print("Default collection: %s" % self.collection)


    # def getMongoClient(self):
    #     return self.client


    def set_database(self, db):
        '''
        set objects' default database
        '''
        self.db = db
        print("Default database: %s" % db)


    def set_collection(self, col):
        '''
        set objects' default collection
        '''
        self.collection = col
        print("Default collection %s" % col)


    def save2db(self, data, db = None, col = None):
        '''
        method: save2db(data, db = None, col = None),
        data = {
            "time": datetime.now()
            "face_class": face_class,
            "prob": prob,
        },
        db: mongodb database, default value = object.db,
        col: mongodb collection, default value = object.collection.
        '''

        if db == None:
            db = self.db
        if col == None:
            col = self.collection
        try:
            mydb = self.client[db]
            mycol = mydb[col]
            mycol.insert_one(data)
            print("Successfully inserted ", str(data), "to ", db + '.' + col)
        except Exception as e:
            print("MongoDB exception: " + str(e))