

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
import tensorflow as tf

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='./fruitresnet100.h5'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224,224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
   # x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    
    
    if preds==0:
         preds="fresh apple"
    elif preds==1:
         preds="fresh banana"
    elif preds==2:
         preds="fresh orange"
    elif preds==3:
         preds="rotten apple"
    elif preds==4:
         preds="rotten banana"
    elif preds==5:
         preds="rotten orange"
    elif preds==6:
         preds="fresh pineapple"
    elif preds==7:
         preds="rotten pineapple"
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('login.html')


@app.route('/about.html', methods=['GET'])
def about():
    # Main page
    return render_template('about.html')
	
	
	
@app.route('/home.html', methods=['GET'])
def home():
    # Main page
    return render_template('home.html')
	

@app.route('/logout.html', methods=['GET'])
def logout():
    # Main page
    return render_template('login.html',msg="logout")
	


@app.route('/login.html', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		username=request.form['username']
		password=request.form['password']
		
		if username=="admin" and password=="admin":
			return render_template('index.html')
		else:
			return render_template('login.html',msg="failed")
		
	else:
		return render_template('login.html')
		
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
