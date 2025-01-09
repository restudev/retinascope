# Retinascope - Deteksi Diabetic Retinopathy

**Retinascope** adalah aplikasi berbasis web yang membantu tenaga medis dalam melakukan diagnosis Diabetic Retinopathy (DR) secara cepat dan akurat menggunakan gambar fundus. Aplikasi ini menggunakan model **MobileNet** untuk mengklasifikasikan gambar fundus ke dalam 5 kelas berdasarkan tingkat keparahan Diabetic Retinopathy, dengan akurasi mencapai **75%**.

## Gambaran Umum Proyek

Diabetic Retinopathy (DR) adalah komplikasi diabetes yang mempengaruhi mata dan dapat menyebabkan kebutaan jika tidak ditangani dengan baik. DR disebabkan oleh kerusakan pada pembuluh darah di retina, bagian mata yang menangkap cahaya. Deteksi dini melalui gambar fundus sangat penting untuk mencegah kerusakan lebih lanjut.

Aplikasi **Retinascope** dirancang untuk membantu tenaga medis dalam mendiagnosis kondisi ini dengan cepat dan akurat menggunakan model **MobileNet**. Aplikasi ini mengklasifikasikan gambar fundus mata ke dalam 5 kelas DR yang berbeda berdasarkan tingkat keparahannya:

1. **No DR** - Tidak ada gejala Diabetic Retinopathy.
2. **Mild DR** - Diabetic Retinopathy ringan.
3. **Moderate DR** - Diabetic Retinopathy sedang.
4. **Severe DR** - Diabetic Retinopathy berat.
5. **Proliferative DR** - DR tingkat lanjut dengan pertumbuhan pembuluh darah abnormal.

## Model dan Akurasi

Model yang digunakan dalam proyek ini adalah **MobileNet**, yang terkenal karena efisiensinya dalam hal kecepatan dan ukuran model, yang membuatnya cocok digunakan pada perangkat dengan sumber daya terbatas. MobileNet menggunakan teknik seperti depthwise separable convolutions untuk membuat model tetap ringan namun akurat dalam mengolah gambar.

- **Model**: MobileNet
- **Akurasi**: 75% pada set pengujian

## Antarmuka Web

Antarmuka pengguna aplikasi **Retinascope** dirancang sederhana dan mudah digunakan. Tenaga medis hanya perlu mengunggah gambar fundus mata, dan aplikasi akan secara otomatis memproses gambar tersebut dan memberikan hasil klasifikasi mengenai tingkat keparahan Diabetic Retinopathy. Proses ini dilakukan dengan cepat dan tidak memerlukan keahlian teknis, memungkinkan tenaga medis untuk mendapatkan diagnosis lebih cepat.

### Screenshot Antarmuka Web

![Halaman Upload dan Prediksi](https://github.com/restudev/retinascope/blob/54ed41a4f079d5e60b7cb543895bbfe86ee14c22/static/img/predict-page.png)
*Halaman Upload dan Prediksi*

![Halaman Dokumentasi](https://github.com/restudev/retinascope/blob/e03bc181e1ed054588eaf2d74d2f2aac67ab71d4/static/img/doc-ui.png)
*Halaman Dokumentasi* 

![Halaman Visualisasi](https://github.com/restudev/retinascope/blob/3f2f529465e0a8e91d5a6af81c3d308e1638e4a8/static/img/visualization-ui.png)
*Halaman Visualisasi*
