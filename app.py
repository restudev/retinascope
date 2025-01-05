from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
from flask_wtf.csrf import CSRFProtect
import secrets
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import requests
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)

# AWS Configuration
AWS_CONFIG = {
    'AWS_ACCESS_KEY_ID': 'AKIA6G75DZIIWB25GNEE',
    'AWS_SECRET_ACCESS_KEY': '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',
    'AWS_REGION': 'ap-southeast-2',
    'AWS_BUCKET_NAME': 'retinascope-prediction-data'
}

def get_s3_client():
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_CONFIG['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=AWS_CONFIG['AWS_SECRET_ACCESS_KEY'],
            region_name=AWS_CONFIG['AWS_REGION']
        )
        return session.client('s3')
    except Exception as e:
        logger.error(f"Failed to initialize S3 client: {str(e)}")
        return None

def upload_to_s3(file_obj, filename):
    try:
        s3_client = get_s3_client()
        if not s3_client:
            raise Exception("Failed to initialize S3 client")

        unique_filename = f"{secrets.token_hex(8)}_{secure_filename(filename)}"
        
        content_type = file_obj.content_type or 'application/octet-stream'
        s3_client.upload_fileobj(
            file_obj,
            AWS_CONFIG['AWS_BUCKET_NAME'],
            unique_filename,
            ExtraArgs={
                'ContentType': content_type
            }
        )
        
        url = f"https://{AWS_CONFIG['AWS_BUCKET_NAME']}.s3.{AWS_CONFIG['AWS_REGION']}.amazonaws.com/{unique_filename}"
        logger.info(f"Successfully uploaded file to S3: {url}")
        return url

    except Exception as e:
        logger.error(f"Error uploading to S3: {str(e)}")
        raise Exception(f"Failed to upload to S3: {str(e)}")

def preprocess_image(file_obj):
    """
    Preprocess image from file object for prediction
    """
    try:
        # Read file into memory
        image_bytes = BytesIO(file_obj.read())
        
        # Reset file pointer for subsequent operations
        file_obj.seek(0)
        
        # Open and process image
        with Image.open(image_bytes) as image:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array

    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise Exception(f"Failed to preprocess image: {str(e)}")

# Flask configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300MB

# CSRF protection
csrf = CSRFProtect(app)

# Load the model
model = load_model('model/model-multi.h5')

# Class mapping
class_mapping = {
    0: 'Mild',
    1: 'Moderate',
    2: 'No DR',
    3: 'Proliferate',
    4: 'Severe'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    try:
        # Read the Excel file using pandas
        EXCEL_FILE_PATH = 'model/dataset.xlsx'  # Make sure this path is correct
        df = pd.read_excel(EXCEL_FILE_PATH)
        data = df.to_dict(orient='records')
        return render_template('documentation.html', data=data)
    except Exception as e:
        logger.error(f"Error in documentation route: {str(e)}")
        return f"An error occurred: {str(e)}"

@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'images[]' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files.getlist('images[]')[0]
        
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format'}), 400

        # First preprocess the image
        preprocessed_image = preprocess_image(file)
        
        # Then upload to S3
        s3_url = upload_to_s3(file, file.filename)
        
        # Make prediction
        predictions = model.predict(preprocessed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])

        response = {
            'predictions': [{
                'filename': file.filename,
                'class_name': class_mapping[predicted_class_idx],
                'prediction_probability': confidence,
                'image_path': s3_url
            }]
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)