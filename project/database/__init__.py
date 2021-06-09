from project.server import db
from os import path
import pandas as pd

csv_path = path.join(path.dirname(path.abspath(__file__)), 'raw_data', 'france.csv')
df = pd.read_csv(csv_path)

STR_FEAT = {'dates', 'scores', 'tm1_names', 'tm2_names'} 
NUM_FEAT = set(df.columns)  - STR_FEAT - {'urls'}

class Matche(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    
    for feat in NUM_FEAT:
        exec(feat + " = db.Column(db.Float, default=True, nullable=False)")
        
    for feat in STR_FEAT:
        exec(feat + " = db.Column(db.String(150), default=True, nullable=False)")

    def __init__(self, row):
        for feat in NUM_FEAT:
            exec(f'self.{feat} = {row[feat]}')
        for feat in STR_FEAT:
            exec(f'self.{feat} = "{row[feat]}"')
