import pymysql
import pickle
import os


def load(f, default):
    if os.path.isfile(f):
        return pickle.load(open(f, "rb"))
    else:
        return default


def connect_to_db():
    conn = pymysql.connect(
        # host='localhost',
        host='delay.doc.ic.ac.uk',
        port=3306,
        user='delay',
        passwd='CcwLCw3Kcs9Py33T',
        db='delay')
    # print('connected to db')
    return conn
