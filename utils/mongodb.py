import pymongo
from datetime import datetime
import cv2
from urllib.parse import quote_plus
from bunch import Bunch
import Notification

class AutofacesMongoDB():

    def __init__(self, config):
        '''
        __init__(self, username, password, host, port, db = None, col = None)
        '''
        # MongoDB info
        dbconfig = Bunch(config.mongodb)

        self.host = dbconfig.host
        self.port = dbconfig.port
        self.db = dbconfig.name
        self.collection = dbconfig.collection

        mongodb_uri = "mongodb://%s:%s"%(self.host, self.port)
        
        print("Connecting to MongoDB...")
        self.client = pymongo.MongoClient(mongodb_uri)
        self.notifier = Notification(Bunch(config.notification))

    def dbinfo(self):
        print("MongoDB host: %s" % self.host)
        print("MongoDB port: %s" % self.port)
        print("Default database: %s" % self.db)
        print("Default collection: %s" % self.collection)

    def save(self, data, db = None, col = None):
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
            mydb = self.client[self.db]
            mycol = mydb[col]
            mycol.insert_one(data)
            print("Successfully inserted ", str(data), "to ", db + '.' + col)
            # print(mycol)
        except Exception as e:
            print("MongoDB exception: " + str(e))

    def create_data(self, frame, pred_clsname, max_prob):
        if not os.path.exists('./datasets/new-frame'):
            os.makedirs('./datasets/new-frame')

        created_time = datetime.now()
        time_str = str(created_time)
        time_str = re.sub('[:-]', '', time_str.split('.')[0])
        time_str = re.sub(' ', '_', time_str)
        image_link = './datasets/new-frame/' + pred_clsname + '_' + time_str + '.jpg'
        try:
            cv2.imwrite(image_link, frame)
        except:
            print("Imwrite error in autoface.createData function.")
        predict_data = {
            "time": created_time,
            'face_class': pred_clsname,
            'prob': float(max_prob),
            'image_link': image_link
        }
        
        # wait 1 seconds to save next image
        next_time_can_save_img = datetime.now() + timedelta(seconds=1)
        return next_time_can_save_img, predict_data

    def save_and_noti(self, frame, pred_clsname, max_prob):
        next_time_can_save_img, predict_data = self.create_data(frame, pred_clsname, max_prob)
        self.save(predict_data)

        if emailNotification.isNewDay(saved_day):
            # reset dict values
            for key in checkin:
                checkin[key] = False
            # renew saved_day
            saved_day = date.today()
        
        if checkin[pred_clsname] is False:
            checkin[pred_clsname] = True
            self.notifier.send_mail(frame, pred_clsname, prob)
