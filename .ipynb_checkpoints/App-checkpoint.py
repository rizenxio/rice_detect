from flask import Flask,render_template,request,jsonify
from keras.models import load_model
import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from datetime import datetime
from keras_preprocessing import image
import numpy as np
app = Flask(__name__)

model = load_model('bahrur-pest-83.48.h5')

UPLOADFOLDER='static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER
ALLOWED_EXTENSION = {'png','jpg','jpeg','webp'}
@app.route('/', methods=['GET','POST'])
#load model for prediction
def main():
    return render_template('index.html')

@app.route('/klasifikasi',methods=['GET','POST'])
def klasifikasi():
     return render_template("klasifikasi.html")

@app.route('/tentang',methods=['GET','POST'])
def tentang():
     return render_template('tentang.html')


@app.route('/penyakit',methods=['GET','POST'])
def penyakit():
     return render_template('penyakit.html')



@app.route('/submit', methods=['POST'])
def predict():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No image in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file:
        # Gunakan nama file asli
        filename = file.filename
        # Simpan file dengan nama aslinya
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Konversi gambar ke RGB
        img = Image.open(file_path).convert('RGB')
        now = datetime.now()
        predict_image_path = os.path.join('static/uploads', now.strftime("%d%m%y-%H%M%S") + "_" + filename)
        img.save(predict_image_path, format='png')
        img.close()
        
        # Persiapkan gambar untuk prediksi
        img = image.load_img(predict_image_path, target_size=(224,224))
        x = image.img_to_array(img)
        x = x/255.0
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        
        # Prediksi
        prediction_array_exception = model.predict(images)
        
        # Persiapkan respon API
        class_names = ['hawar', 'lainnya', 'sehat']
        predicted_class = class_names[np.argmax(prediction_array_exception)]
        confidence = '{:2.0f}%'.format(100 * np.max(prediction_array_exception))
        
        return render_template("klasifikasi.html",
                               img_path=predict_image_path,
                               predictionmodel=predicted_class,
                               confidencemodel=confidence,
                               filename=filename)  # Menambahkan nama file ke template
    else:
        resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg, webp'})
        resp.status_code = 400
        return resp


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)