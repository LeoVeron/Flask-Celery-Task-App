from .manage import cli, app, db
from project.database import df, Matche

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all(app = app)
    db.session.commit()


@cli.command("fill_db")
def fill_db():
    for i, row in df.iterrows():
        matche = Matche(row=row)
        db.session.add(matche)
        db.session.commit()