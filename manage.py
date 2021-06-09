from flask.cli import FlaskGroup

from project.server import create_app, db
from project.database import df, Matche

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
    for i, row in df.iterrows():
        matche = Matche(row=row)
        db.session.add(matche)
        db.session.commit()
    
if __name__ == "__main__":
    cli()