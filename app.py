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

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi AWS untuk akses ke layanan S3
AWS_CONFIG = {
    'AWS_ACCESS_KEY_ID': 'AKIA6G75DZIIWB25GNEE',
    'AWS_SECRET_ACCESS_KEY': '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',
    'AWS_REGION': 'ap-southeast-2',
    'AWS_BUCKET_NAME': 'retinascope-prediction-data'
}

# Fungsi untuk menginisialisasi klien S3
def get_s3_client():
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_CONFIG['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=AWS_CONFIG['AWS_SECRET_ACCESS_KEY'],
            region_name=AWS_CONFIG['AWS_REGION']
        )
        return session.client('s3')
    except Exception as e:
        logger.error(f"Gagal menginisialisasi klien S3: {str(e)}")
        return None

# Fungsi untuk mengunggah file ke S3
def upload_to_s3(file_obj, filename):
    try:
        s3_client = get_s3_client()
        if not s3_client:
            raise Exception("Gagal menginisialisasi klien S3")

        # Membuat nama file unik
        unique_filename = f"{secrets.token_hex(8)}_{secure_filename(filename)}"
        
        # Menentukan tipe konten file
        content_type = file_obj.content_type or 'application/octet-stream'

        # Mengunggah file ke bucket S3
        s3_client.upload_fileobj(
            file_obj,
            AWS_CONFIG['AWS_BUCKET_NAME'],
            unique_filename,
            ExtraArgs={
                'ContentType': content_type
            }
        )
        
        # Membuat URL untuk file yang diunggah
        url = f"https://{AWS_CONFIG['AWS_BUCKET_NAME']}.s3.{AWS_CONFIG['AWS_REGION']}.amazonaws.com/{unique_filename}"
        logger.info(f"Berhasil mengunggah file ke S3: {url}")
        return url

    except Exception as e:
        logger.error(f"Kesalahan saat mengunggah ke S3: {str(e)}")
        raise Exception(f"Gagal mengunggah ke S3: {str(e)}")

# Fungsi untuk memproses gambar sebelum prediksi
def preprocess_image(file_obj):
    try:
        # Membaca file ke dalam memori
        image_bytes = BytesIO(file_obj.read())
        
        # Mengatur ulang pointer file
        file_obj.seek(0)
        
        # Membuka dan memproses gambar
        with Image.open(image_bytes) as image:
            # Konversi ke RGB jika diperlukan
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Mengubah ukuran gambar menjadi 224x224 piksel
            image = image.resize((224, 224))
            
            # Mengonversi ke array numpy dan melakukan normalisasi
            image_array = np.array(image) / 255.0
            
            # Menambahkan dimensi batch
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array

    except Exception as e:
        logger.error(f"Kesalahan saat memproses gambar: {str(e)}")
        raise Exception(f"Gagal memproses gambar: {str(e)}")

# Konfigurasi Flask
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Batas ukuran file 10 MB

# Proteksi CSRF
csrf = CSRFProtect(app)

# Memuat model machine learning
model = load_model('model/model-multi.h5')

# Mapping kelas prediksi ke label
class_mapping = {
    0: 'Mild',
    1: 'Moderate',
    2: 'No DR',
    3: 'Proliferate',
    4: 'Severe'
}

# Fungsi untuk memeriksa file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Rute untuk halaman dokumentasi
@app.route('/documentation')
def documentation():
    try:
        # Membaca file Excel menggunakan pandas
        EXCEL_FILE_PATH = 'model/dataset.xlsx'
        df = pd.read_excel(EXCEL_FILE_PATH)
        data = df.to_dict(orient='records')
        return render_template('documentation.html', data=data)
    except Exception as e:
        logger.error(f"Kesalahan pada rute dokumentasi: {str(e)}")
        return f"Terjadi kesalahan: {str(e)}"

# Rute untuk visualisasi data
@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

# Rute untuk halaman unggah file
@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

# Rekomendasi berdasarkan hasil prediksi
RECOMMENDATIONS = {
    'No DR': {
        "description": "Tidak ditemukan tanda diabetic retinopathy pada pemeriksaan retina. Pembuluh darah di retina terlihat normal tanpa perubahan atau kerusakan yang terdeteksi. Mata dalam kondisi sehat dan tidak ada tanda-tanda gangguan visual akibat diabetes.",
        "specialist": "Dokter Umum atau Spesialis Mata (contoh: dr. Dian Maharani, Sp.M dari JEC)",
        "next_steps": [
            "Lakukan pemeriksaan mata secara berkala minimal satu kali setahun",
            "Pantau kadar gula darah dengan target HbA1c < 7%",
            "Konsumsi makanan sehat rendah gula dan lemak",
            "Lakukan olahraga ringan seperti berjalan kaki 30 menit setiap hari",
            "Jangan lupa istirahat cukup untuk menjaga kesehatan mata"
        ]
    },
    'Mild': {
        "description": "Tanda-tanda awal diabetic retinopathy terdeteksi berupa mikroaneurisma, yaitu pembengkakan kecil pada pembuluh darah retina. Pembuluh darah yang melebar ini dapat menyebabkan kebocoran cairan yang berpotensi menyebabkan gangguan penglihatan ringan. Kondisi ini masih dapat dikelola dengan pengawasan yang tepat.",
        "specialist": "dr. Rina Andayani, Sp.M (Retina Specialist, JEC)",
        "next_steps": [
            "Buat janji temu dengan dokter retina dalam waktu 3-4 bulan",
            "Pantau kadar gula darah dengan target lebih ketat, HbA1c 6.5-7%",
            "Hindari aktivitas yang menyebabkan kelelahan mata seperti menatap layar terlalu lama",
            "Gunakan kacamata pelindung jika diperlukan untuk mengurangi paparan cahaya berlebih",
            "Catat setiap perubahan seperti penglihatan buram atau bintik-bintik gelap"
        ]
    },
    'Moderate': {
        "description": "Diabetic retinopathy tingkat sedang dengan adanya perubahan yang lebih signifikan, termasuk pendarahan kecil (hemorrhage) atau bercak kapas (cotton wool spots) yang merupakan tanda kerusakan pada pembuluh darah retina. Kondisi ini menunjukkan bahwa ada gangguan serius pada suplai darah ke retina yang perlu diatasi dengan penanganan lebih intensif.",
        "specialist": "dr. Andri Santoso, Sp.M (Retina Specialist, JEC)",
        "next_steps": [
            "Jadwalkan konsultasi dengan dokter retina dalam 1-2 bulan",
            "Diskusikan opsi pengobatan seperti laser photocoagulation atau injeksi anti-VEGF",
            "Pantau kadar gula darah ketat, dengan pengukuran harian jika diperlukan",
            "Kurangi aktivitas visual yang membutuhkan fokus tinggi, seperti membaca dalam cahaya redup",
            "Buat jurnal harian untuk mencatat gejala yang dirasakan"
        ]
    },
    'Severe': {
        "description": "Kondisi diabetic retinopathy serius, dengan kerusakan lebih lanjut pada pembuluh darah retina, yang mengarah pada risiko kehilangan penglihatan yang signifikan. Perubahan termasuk pendarahan besar atau pembentukan jaringan parut yang dapat menyebabkan detasemen retina. Tanpa penanganan yang tepat, kondisi ini dapat menyebabkan kebutaan permanen.",
        "specialist": "dr. Yana Oktaviana, Sp.M (Retina Specialist, JEC)",
        "next_steps": [
            "SEGERA konsultasi ke dokter retina, idealnya dalam 1 minggu",
            "Siapkan rencana perawatan intensif seperti laser therapy atau vitrectomy",
            "Pantau gula darah secara ketat di bawah pengawasan dokter ahli endokrin",
            "Hindari mengemudi atau aktivitas berat yang dapat memperburuk kondisi mata",
            "Minta dukungan keluarga atau teman untuk membantu aktivitas sehari-hari"
        ]
    },
    'Proliferate': {
        "description": "Kondisi paling parah dari diabetic retinopathy, dengan pembentukan pembuluh darah baru yang sangat rapuh dan rentan pecah. Pembuluh darah abnormal ini dapat menyebabkan pendarahan berat dan pembentukan jaringan parut yang dapat memisahkan retina dari dinding mata, mengakibatkan kebutaan jika tidak segera ditangani.",
        "specialist": "dr. Maria Christine, Sp.M (Retina Specialist, JEC)",
        "next_steps": [
            "Segera pergi ke unit gawat darurat spesialis mata di JEC",
            "Persiapkan operasi darurat seperti vitrectomy dalam waktu 24-48 jam",
            "Kontrol gula darah intensif di bawah tim medis menggunakan insulin jika diperlukan",
            "Hindari sepenuhnya aktivitas yang membutuhkan ketajaman penglihatan atau membebani mata",
            "Siapkan support system untuk menghadapi proses perawatan dan pemulihan intensif"
        ]
    }
}


# Route untuk mengunggah file
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Memeriksa apakah file dengan key 'images[]' ada dalam permintaan
        if 'images[]' not in request.files:
            return jsonify({'error': 'Tidak ada bagian file'}), 400

        # Mendapatkan file pertama dalam list file
        file = request.files.getlist('images[]')[0]

        # Memeriksa apakah file dipilih
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

        # Memeriksa apakah format file diperbolehkan
        if not allowed_file(file.filename):
            return jsonify({'error': 'Format file tidak valid'}), 400

        # Melakukan preprocess gambar terlebih dahulu
        preprocessed_image = preprocess_image(file)

        # Mengunggah file ke S3
        s3_url = upload_to_s3(file, file.filename)

        # Melakukan prediksi menggunakan model
        predictions = model.predict(preprocessed_image)
        predicted_class_idx = np.argmax(predictions[0])  # Mendapatkan indeks kelas dengan probabilitas tertinggi
        confidence = float(predictions[0][predicted_class_idx])  # Probabilitas kelas yang diprediksi
        predicted_class = class_mapping[predicted_class_idx]  # Nama kelas berdasarkan mapping

        # Mendapatkan rekomendasi berdasarkan kelas yang diprediksi
        recommendation = RECOMMENDATIONS.get(predicted_class, {
            "description": "Silakan konsultasi dengan dokter mata untuk evaluasi lebih lanjut.",
            "specialist": "Dokter Spesialis Mata",
            "next_steps": ["Segera buat janji konsultasi dengan dokter mata"]
        })

        # Membuat respon JSON untuk hasil prediksi
        response = {
            'predictions': [{
                'filename': file.filename,
                'class_name': predicted_class,
                'prediction_probability': confidence,
                'image_path': s3_url,
                'recommendations': recommendation
            }]
        }

        return jsonify(response)  # Mengembalikan hasil prediksi dalam format JSON

    except Exception as e:
        # Logging error jika terjadi masalah
        logger.error(f"Error dalam upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
