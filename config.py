import os

class Config:
    AWS_ACCESS_KEY_ID = os.getenv('AKIA6G75DZIIWB25GNEE')
    AWS_SECRET_ACCESS_KEY = os.getenv('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')
    AWS_BUCKET_NAME = 'retinascope-prediction-data'  # Ganti dengan nama bucket Anda
    AWS_REGION = 'ap-southeast-2'  # Menggunakan Sydney region
