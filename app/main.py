from flask import Flask , request , render_template, url_for , redirect
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import settings
import os
import time
import requests

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

@app.route("/get/job", methods=['GET'])
def GetJob():
    try:
        url = f"http://{settings.API_ENDPOINT}/get/db"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return str(e), 500

@app.route("/get/schedule", methods=['GET'])
def GetSechedule():
    try:
        url = f"http://{settings.API_ENDPOINT}/"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return str(e), 500

@app.route("/pause/<id>", methods=['GET'])
def SetSchedule(id):
    try:
        url = f"http://{settings.API_ENDPOINT}/pause/{id}"
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except Exception as e:
        return str(e), 500

@app.route("/resume/<id>", methods=['GET'])
def DeleteSchedule(id):
    try:
        url = f"http://{settings.API_ENDPOINT}/resume/{id}"
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except Exception as e:
        return str(e), 500
    
if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)