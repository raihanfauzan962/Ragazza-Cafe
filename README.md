# Ragazza Cafe

Proyek ini adalah aplikasi web untuk sistem pemesanan dan manajemen Ragazza Cafe, dibuat dengan **Django**.

## 🚀 Cara Menjalankan Proyek Ini

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di local development environment Anda.

### 1️⃣ Clone repository

```bash
git clone https://github.com/raihanfauzan962/Ragazza-Cafe.git
cd Ragazza-Cafe
```

### 2️⃣ (Opsional) Buat virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux / MacOS
venv\Scripts\activate          # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum ada atau ingin membuatnya:

```bash
pip freeze > requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Buat superuser

```bash
python manage.py createsuperuser
```

Ikuti instruksi untuk mengisi username, email, dan password.

### 6️⃣ Jalankan server

```bash
python manage.py runserver
```

Buka browser dan akses:

```
http://127.0.0.1:8000/
```

### 7️⃣ Update requirements (jika menambah paket baru)

```bash
pip freeze > requirements.txt
```

## 📄 Dokumentasi

Berikut dokumentasi terkait proyek ini:

* [Dokumentasi Proyek (Umum)](https://docs.google.com/document/d/1z4IElPlqOeyhawAsNEEqHfFZUJUK2Jbgx7HC8kNjyNw/edit?usp=sharing)
* [Dokumentasi Database dan Model](https://docs.google.com/document/d/13AHS_nYPlWoxDSQvewwL2EYXFZXerAJcQnHeBpGtPT0/edit?usp=sharing)
* [Dokumentasi Alur Sistem](https://docs.google.com/document/d/1WFde5tcLUsJxvBuzsYsYFc089UsoBGuUVqTCcZamFAw/edit?usp=sharing)

## 💻 Repository

[https://github.com/raihanfauzan962/Ragazza-Cafe](https://github.com/raihanfauzan962/Ragazza-Cafe)

---

## ✨ Catatan

* Pastikan Anda sudah menginstall Python 3.7+.
* Anda bisa menambahkan env file jika ada pengaturan seperti secret key, database, dsb.
* Jangan lupa untuk memeriksa konfigurasi `settings.py` jika ingin menggunakan database production (misal PostgreSQL).
