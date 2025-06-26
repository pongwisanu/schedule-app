from flask import Flask, request, jsonify , url_for
from extension import scheduler , mongo
from celery_trigger import first_trigger
from pymongo.errors import ConnectionFailure
from config import settings
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

@app.route("/get/db", methods=['GET'])
def GetDB():
    try:
        result = mongo.schedule.job.find()
        job_list = []
        for job in result:
            obj = {
                "id": job['id'],
                "trigger": job['trigger'],
                "created_date": job['created_date']
            }
            job_list.append(obj)
        return job_list
    except Exception as e:
        return str(e)

@app.route("/get/trigger", methods=['GET'])
def GetTrigger():
    try:
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
    except Exception as e:
        return str(e)

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
            trigger_type = "cron"
            trigger_args = {
                "minute": "*"
            }
            
            job = AddJob(id, trigger_type, trigger_args)
            
            JOB_COLLECTION.insert_one({
                "id": id,
                "trigger": trigger_args,
                "status": "enable",
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
        result = mongo.schedule.job.find_one({"id":id})
        if result is None:
            raise Exception("'%s' does not exist" % id)
        scheduler.pause_job(id)
        mongo.schedule.job.update_one(
            {"id": id},
            {'$set' : {"status": "disable"}}
        )
        return "Pause job name %s" % id
    except Exception as e:
        return str(e)

@app.route("/resume/<id>", methods=['GET'])
def ResumeJob(id):
    try:
        result = mongo.schedule.job.find_one({"id":id})
        if result is None:
            raise Exception("'%s' does not exist" % id)

        try:
            scheduler.resume_job(id)
        except Exception as e:
            if("No job by the id" in str(e)):
                AddJob(result['id'], "cron", result['trigger'])
            else:
                raise Exception(e)
            
        mongo.schedule.job.update_one(
            {"id": id},
            {'$set' : {"status": "enable"}}
        )
        return "Resume job name %s" % id
    except Exception as e:
        return str(e)

@app.route("/delete/<id>", methods=['GET'])
def DeleteJob(id):
    try:
        result = mongo.schedule.job.find_one({"id":id})
        if result is None:
            raise Exception("'%s' does not exist" % id)
        scheduler.remove_job(id)
        mongo.schedule.job.delete_one({"id":id})
        return "Delete job name %s" % id
    except Exception as e:
        return str(e)

def AddJob(id:str, trigger_type:str, trigger_args:dict):
    func = GetFunctionFromString(id)
    job = scheduler.add_job(
        func=func,
        trigger=trigger_type,
        **trigger_args,
        id=id,
        name=id,
        replace_existing=True,
    )
    
    return job

def EditJob(id:str, trigger_type:str, trigger_args:dict):
    return

def InitializeSchedule():
    result = mongo.schedule.job.find()
    for i in result:
        try:
            if i['status'] == "enable":
                id = i['id']
                trigger_type = "cron"
                trigger_args = i['trigger']
                job = AddJob(id, trigger_type, trigger_args)
                print("Successful initailize '%s' from database" % job.name)
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