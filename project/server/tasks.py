import os
import time


from project.database import Matche
from project.server import create_app
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


# @celery.task(base=SqlAlchemyTask)
# def get_from_db(user_id):
#     user = db_session.query(User).filter(User.id=user_id).one()
#     # do something with the user
    





@celery.task(name="create_task", base=SqlAlchemyTask)
def create_task(match_id):
    match = db_session.query(Matche).filter(Matche.id == match_id).one()
    match_name = match.dates
    # app=create_app(register_blueprints=False)
    # with app.app_context():
    #     match = Matche.query.get(match_id)
    # match_name = match.dates
    return match_name



