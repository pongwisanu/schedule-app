from flask import Flask, request, jsonify
from extension import scheduler
from celery_trigger import first_trigger
import time
import datetime
import atexit
import json

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
    
@app.route("/add", methods=['GET'])
def AddJob():
    job = scheduler.add_job(
        func=first_trigger.FirstTrigger,
        trigger="interval",
        seconds=20,
        id="first_trigger",
        name="first_trigger",
        replace_existing=True,
    )
    return "Add job name %s" % job.name
    
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
    
if __name__ == "__main__":
    with app.app_context():
        # Initialize default schedule if exist
        from celery_trigger import first_trigger
        
        scheduler.start()
           
    app.run("0.0.0.0", 5000)