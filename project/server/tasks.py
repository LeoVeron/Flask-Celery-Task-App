import os
import time
import pandas as pd

from project.database import Matche
from project.server.model.data_prep import create_X
from project.server.model.predict import predict
from celery import Celery
# import celery

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

engine = create_engine(
    'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev', convert_unicode=True,
    pool_recycle=3600, pool_size=10)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@celery.task(name="create_task", base=SqlAlchemyTask)
def create_task(match_id):
    start_time = time.time()
    
    df = pd.read_sql(db_session.query(Matche).filter(Matche.id == match_id).statement,db_session.bind) 
    # match = db_session.query(Matche).filter(Matche.id == match_id).one()
    
    match_name = f"{df.iloc[0]['tm1_names']} {df.iloc[0]['tm2_names']} {df.iloc[0]['dates']}"

    #preprocess X
    df = pd.read_sql(db_session.query(Matche).filter(Matche.id == match_id).statement,db_session.bind) 
    X= create_X(df)

    #model prediction
    prediction = predict(X)
    prediction = [int(x*100) for x in prediction[0]]
    
    #time use for prediction + adding time for example
    time.sleep(2)
    restime = round(time.time() - start_time,2)
    
    return match_name, restime, prediction

