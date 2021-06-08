from project.server import db
from os import path
import pandas as pd

csv_path = path.join(path.dirname(path.abspath(__file__)), 'raw_data', 'france.csv')
df = pd.read_csv(csv_path)
STR_FEAT = {'dates', 'scores', 'tm1_names', 'tm2_names'} 
BOOL_FEAT = set(df.columns)  - STR_FEAT - {'urls'}
ALL_FEAT= STR_FEAT | BOOL_FEAT

class Matche(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    
    for feat in BOOL_FEAT:
        exec(feat + " = db.Column(db.Boolean(), default=True, nullable=False)")
        
    for feat in STR_FEAT:
        exec(feat + " = db.Column(db.String(150), default=True, nullable=False)")

    def __init__(self, row):
        for feat in ALL_FEAT:
            exec(f'self.{feat} = {row[feat]}')
        
def upload_csv_matche(db):
    for row in df.iterrows():
        matche = Matche(row=row)
        db.session.add(matche)
        db.session.commit()