from extension import celery

def FirstTrigger():
    print("This is schedule FirstTrigger")
    celery.send_task("first_trigger")