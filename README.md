# Math Genius v1.0

## Deskripsi Proyek

Math Genius v1.0 adalah aplikasi kuis matematika interaktif yang dirancang khusus untuk siswa sekolah dasar kelas 1. Aplikasi ini bertujuan untuk membantu anak-anak melatih kemampuan berhitung dasar mereka dengan cara yang menyenangkan dan memotivasi. Soal-soal kuis dihasilkan secara acak untuk setiap sesi, memastikan pengalaman belajar yang bervariasi.

Aplikasi ini juga dilengkapi dengan fitur penyimpanan skor dan riwayat untuk melacak kemajuan pelajar, serta dukungan multibahasa (Bahasa Indonesia dan Bahasa Inggris).

## Fitur Utama

- **Tingkatan SD Kelas 1**: Soal-soal matematika dasar (penjumlahan, pengurangan, perkalian sederhana, pembagian sederhana) yang disesuaikan untuk tingkat kelas 1 SD.
- **Soal Acak**: Setiap sesi kuis menyajikan 10 pertanyaan yang dihasilkan secara acak, memastikan variasi dan tantangan baru setiap kali bermain.
- **Sistem Skor**: Pengguna mendapatkan 10 poin untuk setiap jawaban yang benar.
- **Penyimpanan Skor**: Nama dan skor pengguna disimpan secara otomatis di file `data.json` di folder `save`. Skor tertinggi akan ditampilkan di riwayat.
- **Riwayat Skor**: Riwayat skor sebelumnya ditampilkan di menu utama untuk memotivasi pelajar dan menunjukkan kemajuan mereka.
- **Dukungan Multi-Bahasa**: Aplikasi mendukung Bahasa Indonesia dan Bahasa Inggris, dengan opsi pemilihan bahasa yang mudah diakses di menu utama.
- **Antarmuka Pengguna Grafis (GUI)**: Dibangun dengan PyQt5, menyediakan antarmuka yang intuitif dan mudah digunakan.

## Cara Menjalankan Aplikasi

### Prasyarat

Pastikan Anda telah menginstal Python 3.x. Anda juga memerlukan pustaka PyQt5. Jika belum terinstal, Anda bisa menginstalnya menggunakan pip:

```bash
pip install PyQt5
```

### Langkah-langkah

#### 1. Kloning Repositori (jika dari GitHub)

```bash
git clone https://github.com/nama-pengguna-anda/math-genius-v1.0.git
cd math-genius-v1.0
```

Ganti `nama-pengguna-anda` dengan username GitHub Anda dan `math-genius-v1.0` dengan nama repositori Anda.

#### 2. Unduh Kode (jika tidak dari GitHub)

Jika Anda mendapatkan kode ini secara langsung (misalnya, dari file ZIP), pastikan semua file berada dalam satu folder.

#### 3. Buat Folder `save`

Di dalam direktori utama proyek (tempat file `math_quiz.py` berada), buat folder baru bernama `save`. Aplikasi akan menyimpan data skor di folder ini.

```bash
mkdir save
```

#### 4. Jalankan Aplikasi

Buka terminal atau command prompt, navigasikan ke direktori proyek Anda, lalu jalankan skrip Python:

```bash
python math_quiz.py
```

## Struktur File

```
.
├── math_quiz.py        # Kode sumber utama aplikasi
└── save/               # Direktori untuk menyimpan data skor
    └── data.json       # File JSON yang berisi riwayat skor
```

## Kontribusi

Kontribusi sangat dihargai! Jika Anda memiliki saran, perbaikan bug, atau fitur baru yang ingin ditambahkan, silakan buka *issue* atau kirim *pull request*.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Dibuat dengan ❤️ oleh [HusenAJ]

