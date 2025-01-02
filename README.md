# Klasifikasi Retinopati Diabetik

Proyek ini berfokus pada klasifikasi Retinopati Diabetik (DR) berdasarkan gambar fundus menggunakan model **MobileNet**. Model ini mencapai akurasi **75%** untuk mengklasifikasikan DR ke dalam 5 kelas.

## Gambaran Umum Proyek

Retinopati Diabetik (DR) adalah komplikasi diabetes yang mempengaruhi mata. Hal ini disebabkan oleh kerusakan pada pembuluh darah jaringan sensitif cahaya di bagian belakang mata (retina). Deteksi dini melalui gambar fundus sangat penting untuk mengelola dan mengobati kondisi ini secara efektif.

Proyek ini menggunakan model **MobileNet** untuk mengklasifikasikan gambar fundus ke dalam 5 kelas Retinopati Diabetik yang berbeda:

1. No DR
2. Mild DR
3. Moderate DR
4. Severe DR
5. Proliferative DR

## Model dan Akurasi

Model yang digunakan dalam proyek ini didasarkan pada **MobileNet**, sebuah arsitektur jaringan saraf konvolusional yang dirancang untuk perangkat dengan keterbatasan sumber daya, dengan memberikan efisiensi tinggi dalam hal komputasi dan ukuran model. MobileNet menggunakan teknik seperti depthwise separable convolutions untuk mengurangi kompleksitas model.

- **Model**: MobileNet
- **Akurasi**: 75% pada set pengujian

## Antarmuka Web

Untuk membuat model ini dapat diakses, sebuah antarmuka web sederhana dibuat. Pengguna dapat mengunggah gambar fundus, dan model akan memprediksi tahap Retinopati Diabetik.

### Screenshot Antarmuka Web

![Halaman Utama](https://github.com/restudev/retinascope/blob/d02b8e95447ac29568ede0ef79b595a7329a6fef/upload-ui.png)

*Keterangan: Halaman utama antarmuka web.*
