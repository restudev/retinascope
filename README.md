# Klasifikasi Diabtic Retinopathy

Proyek ini berfokus pada klasifikasi Diabtic Retinopathy (DR) berdasarkan gambar fundus menggunakan model **MobileNet**. Model ini mencapai akurasi **75%** untuk mengklasifikasikan DR ke dalam 5 kelas berdasarkan tingkat keparahannya.

## Gambaran Umum Proyek

Diabtic Retinopathy (DR) adalah komplikasi diabetes yang mempengaruhi mata. Hal ini disebabkan oleh kerusakan pada pembuluh darah jaringan sensitif cahaya di bagian belakang mata (retina). Deteksi dini melalui gambar fundus sangat penting untuk mengelola dan mengobati kondisi ini secara efektif.

Proyek ini menggunakan model **MobileNet** untuk mengklasifikasikan gambar fundus ke dalam 5 kelas Diabtic Retinopathy yang berbeda:

1. No DR
2. Mild DR
3. Moderate DR
4. Severe DR
5. Proliferative DR

## Model dan Akurasi

Model yang digunakan dalam proyek ini adalah **MobileNet**, sebuah arsitektur jaringan saraf yang dirancang untuk efisiensi tinggi, terutama pada perangkat dengan keterbatasan sumber daya. MobileNet menggunakan teknik canggih, seperti depthwise separable convolutions, untuk membuat model tetap ringan namun tetap akurat dalam mengolah gambar. Dengan cara ini, model dapat bekerja cepat tanpa mengorbankan kinerja.

- **Model**: MobileNet
- **Akurasi**: 75% pada set pengujian

## Antarmuka Web

Antarmuka web untuk model ini dirancang sederhana dan mudah digunakan. Pengguna cukup mengunggah gambar fundus mata, lalu model akan secara otomatis memproses gambar tersebut dan memberikan prediksi tentang tingkat keparahan Diabtic Retinopathy. Prosesnya cepat dan langsung, sehingga memudahkan siapa saja untuk menggunakan model ini tanpa memerlukan keahlian teknis.

### Screenshot Antarmuka Web

<img src="https://github.com/restudev/retinascope/blob/566438595976da50f1becb5095d536a21746b22a/static/img/upload-ui.png" alt="Halaman Upload" width="200" />

*Keterangan: Halaman upload/predict.*
