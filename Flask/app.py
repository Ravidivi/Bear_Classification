from flask import Flask, render_template, request, jsonify, url_for, redirect
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app = Flask(__name__, template_folder='template')

model = tf.keras.models.load_model('bear_classifier.h5')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict')
def predict():
    return render_template("inner-page.html")

@app.route('/output', methods=['GET','POST'])
def output():
    if request.method =='POST':
        f=request.files['file']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        img=load_img(filepath,target_size=(64,64))
        # Resize the image to the required size
        # Convert the image to an array and normalize it
        image_array = np.array(img)
        # Add a batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        # Use the pre-trained model to make a prediction
        pred=np.argmax(model.predict(image_array),axis=1)
        index=['black','gaint_panda','polar','red_panda']

        prediction = index[int(pred)]
        print("prediction")
        #predict = prediction
        return render_template("output.html", predict = prediction)
    
@app.route('/contact')
def contact():
    return render_template("index.html")


if __name__=='__main__':
    app.run(debug = True,port = 2222)