from extension import celery

def SecondTrigger():
    print("This is schedule SecondTrigger not initialize from database but can set though api")
    celery.send_task("second_trigger")