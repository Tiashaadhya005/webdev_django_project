from pymongo import MongoClient

#uri ="mongodb://mongo/"
#client= MongoClient(uri)
client=MongoClient('localhost', 27017)


mydb=client['busbooking']

def get_db():
    return mydb

def get_coll_for_user_acc():
    c='userdetails'
    return mydb[c]