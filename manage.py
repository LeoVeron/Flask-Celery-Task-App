from flask.cli import FlaskGroup

from project.server import create_app, db
from project.database import Matche, upload_csv_matche

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(email="michael@mherman.org"))
#     db.session.commit()

@cli.command("fill_db")
def fill_db():
    upload_csv_matche()
    
if __name__ == "__main__":
    cli()