from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from datetime import datetime
from keras_preprocessing import image
import numpy as np
import secrets
from keras.models import load_model
from werkzeug.utils import secure_filename

# Load the model
try:
    model = load_model('bahrur-pest-89.99.h5')
except Exception as e:
    print(f"Error loading model: {str(e)}")

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure random secret key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/klasifikasi')
def klasifikasi():
    return render_template("klasifikasi.html")

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/penyakit')
def penyakit():
    return render_template('penyakit.html')

@app.route('/submit', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No image in the request', 'error')
        return redirect(url_for('klasifikasi'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected for uploading', 'error')
        return redirect(url_for('klasifikasi'))
    
    if not allowed_file(file.filename):
        flash('Allowed file types are png, jpg, jpeg, webp', 'error')
        return redirect(url_for('klasifikasi'))
        
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        
        # Create full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the uploaded file
        file.save(file_path)
        
        # Process image for prediction
        with Image.open(file_path).convert('RGB') as img:
            # Resize and preprocess image
            img_processed = img.resize((256, 256))
            img_array = image.img_to_array(img_processed)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            prediction_array = model.predict(img_array)
            
            # Get prediction results
            class_names = ['hawar', 'lainnya', 'sehat']
            predicted_class = class_names[np.argmax(prediction_array)]
            confidence = '{:2.0f}%'.format(100 * np.max(prediction_array))
            
            flash('Image processed successfully!', 'success')
            
            return render_template(
                "klasifikasi.html",
                img_path=file_path,
                predictionmodel=predicted_class,
                confidencemodel=confidence,
                filename=filename
            )
                            
    except Exception as e:
        flash(f'Error processing image: {str(e)}', 'error')
        return redirect(url_for('klasifikasi'))

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('klasifikasi'))

@app.errorhandler(500)
def internal_error(e):
    flash('An internal server error occurred. Please try again later.', 'error')
    return redirect(url_for('klasifikasi'))

@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)