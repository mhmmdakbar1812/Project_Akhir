from flask import Flask, render_template, request, jsonify, redirect, url_for
import numpy as np
from urllib.parse import unquote
import base64
#from flask_ngrok import run_with_ngrok
from PIL import Image
from flask import session
import io
import tensorflow as tf
from tensorflow import keras
import cv2
import os


app = Flask(__name__, static_url_path='/static')
#run_with_ngrok(app)
app.secret_key = 'ribet_beut_sumpah'

# route for home page (desktop__1)
@app.route('/', methods=['GET'])
def home():
    return render_template('desktop___1.html')


# route for capturing image (desktop__2)
@app.route('/capture_image', methods=['GET', 'POST'])
def capture_image():
    if request.method == 'GET':
        return render_template('desktop___2.html')
    elif request.method == 'POST':
        image_data = request.files['capture']
        # Convert the image data to base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        # Redirect to the process_download endpoint and pass the image data as a query parameter
        return redirect(url_for('process_download', capture=image_base64))

@app.route('/process_download', methods=['GET', 'POST'])
def process_download():
    if request.method == 'POST':
        image_data = request.files['capture']
        
        if image_data is None:
            return jsonify({'error': 'No image data provided.'}), 400
        
        # Save the downloaded file to a temporary directory
        temp_filepath = 'static/temp/capture.jpeg'
        image_data.save(temp_filepath)
        
        # Perform image processing as before
        img = Image.open(temp_filepath)
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        if predicted_class >= 0.5:
            label = 'Open Eyes'
        else:
            label = 'Closed Eyes'
        
        # Remove the temporary file after processing is done
        # os.remove(temp_filepath)
        session['label'] = label
        # Redirect to the result page with the prediction as a query parameter
        return redirect(url_for('show_result'))

@app.route('/show_result')
def show_result():
    # Get the prediction from the query parameter
    label = session.get('label')
    print(label)
    if label:
        if label == 'Open Eyes':
            prediction = 'Mata Terbuka'
        elif label == 'Closed Eyes':
            prediction = 'Mata Tertutup'
        else:
            prediction = 'Prediksi tidak valid'
    else:
        prediction = 'Label tidak tersedia'
     
    # Render the template with the prediction
    return render_template('desktop___3.html', prediction=prediction)

if __name__ == '__main__':
    # load the model
    #optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, decay=1e-6)
    model = tf.keras.models.load_model("Drowsiness_model.h5")
    app.run()