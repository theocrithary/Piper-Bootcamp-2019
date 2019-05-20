#!/usr/bin/env python3

#########################################################
# This is the database processing file. (aka. Models)
# It contains the DB connections, queries and processes
# principles of Models, Views, Controllers (MVC).
#########################################################

# Import modules required for app
import os
from pymongo import MongoClient
from werkzeug import secure_filename

# Check if running in Pivotal Web Services with MongoDB service bound
if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    MONGOCRED = VCAP_SERVICES["mlab"][0]["credentials"]
    client = MongoClient(MONGOCRED["uri"])
    DB_NAME = str(MONGOCRED["uri"].split("/")[-1])

# Otherwise, assume running locally with local MongoDB instance    
else:
    client = MongoClient('127.0.0.1:27017')
    DB_NAME = "mongodb"  ##### Make sure this matches the name of your MongoDB database ######

# Get database connection with database name
db = client[DB_NAME]

# Retrieve all photos records from database
def get_photos():
    return db.photos.find({})

# Insert form fields into database
def insert_photo(request):
    title = request.form['title']
    comments = request.form['comments']
    filename = secure_filename(request.files['photo'].filename)
    thumbfile = filename.rsplit(".",1)[0] + "-thumb.jpg"

    db.photos.insert_one({'title':title, 'comments':comments, 'photo':filename, 'thumb':thumbfile})