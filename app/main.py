from flask import Flask , request , render_template, url_for , redirect
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import settings

import os
import time

try:
    CLIENT = MongoClient(
            settings.DSN,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
    CLIENT.admin.command('ping')
    print(f"Connection to DB Successful", flush=True)
except ConnectionFailure as e:
    print(f"Connection Failure : {e}", flush=True)
    os._exit(1)

app = Flask(__name__)

@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/get/schedule", methods=['GET'])
def GetSchedule():
    JOB = CLIENT['account']['job']
    result = JOB.find()
    
    list_job = []
    for i in result:
        new_obj = {
            
        }
        list_job.append(new_obj)
            
    return list_job

@app.route("/get/file/job", methods=['GET'])
def GetFileJob():
    files = os.listdir(settings.JOB_PATH)
    files_list_obj = []
    for i in files:
        file_path = os.path.join(settings.JOB_PATH, i)
        new_obj = {
            "file_path": file_path,
            "file_name": i,
            "create_date": time.ctime(os.path.getctime(file_path))
        }
        files_list_obj.append(new_obj)
    return files_list_obj

@app.route("/add/schedule", methods=['POST'])
def SetSchedule():
    return ""

@app.route("/delete/schedule", methods=['DELETE'])
def DeleteSchedule():
    return ""
    
if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)