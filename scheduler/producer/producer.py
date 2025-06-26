from flask import Flask, request, jsonify , url_for
from extension import scheduler , mongo
from celery_trigger import first_trigger
from pymongo.errors import ConnectionFailure
import time
import datetime
import atexit
import json
import os
import importlib
import requests

try:
    mongo.admin.command('ping')
    print(f"Connection to DB Successful", flush=True)
except ConnectionFailure as e:
    print(f"Connection Failure : {e}", flush=True)
    os._exit(1)

app = Flask(__name__)

scheduler.init_app(app)

@app.route("/", methods=['GET'])
def GetAll():
    try: 
        result = scheduler.get_jobs()
        job_list = []
        for job in result:
            job_data = {
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time),
                "trigger": str(job.trigger),
                "func": str(job.func_ref),
                "args": job.args,
                "kwargs": job.kwargs
            }
            job_list.append(job_data)
        return jsonify({"result" : job_list})
    except Exception as e:
        return str(e)

@app.route("/get/trigger", methods=['GET'])
def GetTrigger():
    return

@app.route("/get/<id>", methods=['GET'])
def GetJob(id):
    try:
        result = scheduler.get_job(id)
        if result is None:
            raise Exception("Job id is not exist")
        job_data = {
            "id": result.id,
            "name": result.name,
            "next_run_time": str(result.next_run_time),
            "trigger": str(result.trigger),
            "func": str(result.func_ref),
            "args": result.args,
            "kwargs": result.kwargs
        }
        return jsonify({"result": job_data})
    except Exception as e:
        return str(e)
    
@app.route("/add/<id>", methods=['GET'])
def AddJob(id):
    
    try:
        JOB_COLLECTION = mongo.schedule.job
        
        res = JOB_COLLECTION.find_one({"id":id})
        
        if res is None:
            func = GetFunctionFromString(id)
            
            trigger_type = "cron"
            trigger_args = {
                "minute": "*"
            }
            
            job = scheduler.add_job(
                func=func,
                trigger=trigger_type,
                **trigger_args,
                id=id,
                name=id,
                replace_existing=True,
            )
            
            
            JOB_COLLECTION.insert_one({
                "id": id,
                "trigger": trigger_args,
                "created_date": datetime.datetime.now()
            })
                    
            return "Add job name %s" % job.name
        else: 
            raise Exception("This job %s is already exist" % id)
    except Exception as e:
        return str(e)
    
@app.route("/pause/<id>", methods=['GET'])  
def PauseJob(id):
    try:
        scheduler.pause_job(id)
        return "Pause job name %s" % id
    except Exception as e:
        return str(e)

@app.route("/resume/<id>", methods=['GET'])
def ResumeJob(id):
    try:
        scheduler.resume_job(id)
        return "Resume job name %s" % id
    except Exception as e:
        return str(e)

@app.route("/delete/<id>", methods=['GET'])
def DeleteJob(id):
    try:
        scheduler.remove_job(id)
        return "Delete job name %s" % id
    except Exception as e:
        return str(e)

def InitializeSchedule():
    result = mongo.schedule.job.find()
    for i in result:
        try:
            url = url_for("AddJob", id=i['id'])
            res = requests.get(url)
            res.raise_for_status()
        except Exception as e:
            print(str(e))
    
def GetFunctionFromString(path):
    module_name, func_name = path.rsplit('.',1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)
    
if __name__ == "__main__":
    with app.app_context():
        # Initialize default schedule if exist
        from celery_trigger import first_trigger
        
        scheduler.start()
           
        InitializeSchedule()
           
    app.run("0.0.0.0", 5000)