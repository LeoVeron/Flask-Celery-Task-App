import os
import time


from project.database import Matche
from project.server import create_app
from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


# @celery.task(name="create_task")
# def create_task(match_id):
#     # time.sleep(2)
    
#     #fetching datas
#     match = Matche.query.get(match_id)
#     match_name = match.dates
    
#     #preprocess X
    
#     #model prediction
#     prediction = [1,0,0]
    
#     #time use maybe?
#     restime = 1
#     return True
#     return match_name, restime, prediction
    


@celery.task(name="create_task")
def create_task(match_id):
    app=create_app(register_blueprints=False)
    with app.app_context():
        match = Matche.query.get(match_id)
    match_name = match.dates
    return match_name