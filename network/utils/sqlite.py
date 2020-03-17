import sqlite3
import sys

class Top3Helper:
    def __init__(self, dbpath):
        self.create_connection(dbpath)
        self.create_table_if_doest_exist()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:#Exception as e:
            #print(e)
            print ("Error %s:" % e.args[0])
            sys.exit(1)
    
        return self.conn

    def create_table_if_doest_exist(self):
        sql = ''' CREATE TABLE IF NOT EXISTS top3_predict (
                    Id INTEGER PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    top1 TEXT NOT NULL,
                    prob1 DOUBLE NOT NULL,
                    top2 TEXT NOT NULL,
                    prob2 DOUBLE NOT NULL,
                    top3 TEXT NOT NULL,
                    prob3 DOUBLE NOT NULL
                )'''
                #,checkin_date DATETIME NOT NULL
        cur = self.conn.cursor()
        cur.execute(sql)   

    def add_predict(self, filepath, top3):
        # data = {
        #     'file_path':filepath,
        #     'top1':top3[0][0],
        #     'prob1':top3[0][1],
        #     'top2':top3[1][0],
        #     'prob2':top3[1][1],
        #     'top3':top3[2][0],
        #     'prob3':top3[2][1],
        # }
        data = ('%s'%(filepath), top3[0][0], top3[0][1], top3[1][0], top3[1][1], top3[2][0], top3[2][1])
        #print(data)
        sql = ''' INSERT INTO top3_predict(file_path, top1, prob1, top2, prob2, top3, prob3)
                     VALUES(?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data)
        #cur.execute("SELECT * FROM top3_predict")
        #rows = cur.fetchall()
        #for row in rows:
        #    print(row)
        return cur.lastrowid