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

@app.route("/add", methods=['POST'])
def SetSchedule():
    return ""

@app.route("/delete", methods=['DELETE'])
def DeleteSchedule():
    return ""
    
if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)