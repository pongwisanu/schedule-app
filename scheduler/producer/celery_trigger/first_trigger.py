from extension import celery

def FirstTrigger():
    print("This is schedule FirstTrigger must be initialize from database")
    celery.send_task("first_trigger")