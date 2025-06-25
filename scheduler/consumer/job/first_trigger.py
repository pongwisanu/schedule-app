from consumer import celery
import socket

@celery.task(name="first_trigger")
def FirstTriggerJob():
    print(f"This is {socket.gethostname()}")