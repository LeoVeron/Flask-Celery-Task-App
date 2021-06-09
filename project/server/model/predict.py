from tensorflow.keras import models
import tensorflow_addons as tfa
import os

def predict(X): 
    dirname = os.path.dirname(__file__)
    model_path = os.path.join(dirname,'model.h5')
    model = models.load_model(model_path)
    return model.predict(X)
    