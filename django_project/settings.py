# Impor Path dari pathlib untuk menangani jalur file secara portabel di berbagai sistem operasi.
from pathlib import Path

# Mendefinisikan BASE_DIR sebagai direktori utama proyek.
# Path(__file__).resolve().parent.parent mengambil direktori dua tingkat di atas file ini (settings.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Pengaturan untuk pengembangan cepat, tidak cocok untuk produksi.
# Lihat dokumentasi Django untuk daftar periksa penyebaran: https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# Peringatan keamanan: SECRET_KEY harus dirahasiakan di lingkungan produksi.
# Kunci ini digunakan untuk keamanan kriptografi seperti sesi dan token.
SECRET_KEY = "django-insecure-hv1(e0r@v4n4m6gqdz%dn(60o=dsy8&@0_lbs8p-v3u^bs4)xl"

# Peringatan keamanan: Jangan aktifkan DEBUG di produksi karena dapat menampilkan informasi sensitif.
# DEBUG = True mempermudah debugging selama pengembangan.
DEBUG = True

# Daftar host yang diizinkan untuk mengakses aplikasi.
# Kosong berarti hanya localhost diizinkan saat DEBUG = True.
ALLOWED_HOSTS = []

# Daftar aplikasi yang diinstal dalam proyek.
INSTALLED_APPS = [
    # Aplikasi bawaan Django untuk fungsi inti.
    "django.contrib.admin",  # Antarmuka admin Django.
    "django.contrib.auth",  # Sistem otentikasi pengguna.
    "django.contrib.contenttypes",  # Sistem tipe konten untuk model.
    "django.contrib.sessions",  # Manajemen sesi pengguna.
    "django.contrib.messages",  # Sistem pesan sementara untuk pengguna.
    "django.contrib.staticfiles",  # Manajemen file statis (CSS, JS, gambar).
    "django.contrib.sites",  # Dukungan untuk multi-situs (diperlukan oleh django-allauth).
    # Aplikasi pihak ketiga.
    "allauth",  # Django-allauth untuk otentikasi dan manajemen akun.
    "allauth.account",  # Modul akun dari django-allauth.
    # Aplikasi lokal yang dibuat dalam proyek.
    "accounts.apps.AccountsConfig",  # Aplikasi untuk model pengguna kustom.
    "pages.apps.PagesConfig",  # Aplikasi untuk halaman statis atau dinamis.
    "cafe.apps.CafeConfig",  # Aplikasi untuk fungsi restoran (menu, pesanan, dll.).
]

# Daftar middleware yang memproses permintaan dan respons HTTP.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Menangani pengaturan keamanan HTTP.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Mengelola sesi pengguna.
    "django.middleware.common.CommonMiddleware",  # Menangani fitur umum seperti URL trailing slash.
    "django.middleware.csrf.CsrfViewMiddleware",  # Melindungi dari serangan CSRF.
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Menangani otentikasi pengguna.
    'allauth.account.middleware.AccountMiddleware',  # Middleware untuk django-allauth.
    "django.contrib.messages.middleware.MessageMiddleware",  # Menangani pesan sementara.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Melindungi dari serangan clickjacking.
]

# Menentukan modul URL utama proyek (file urls.py di direktori proyek).
ROOT_URLCONF = "django_project.urls"

# Konfigurasi template untuk rendering HTML.
TEMPLATES = [
    {
        # Menggunakan backend template bawaan Django.
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Direktori tambahan untuk template di luar aplikasi (BASE_DIR/templates).
        "DIRS": [BASE_DIR / "templates"],
        # Mengaktifkan pencarian template di direktori aplikasi (misalnya cafe/templates).
        "APP_DIRS": True,
        # Opsi tambahan untuk prosesor konteks template.
        "OPTIONS": {
            "context_processors": [
                # Menambahkan variabel debug ke konteks template.
                "django.template.context_processors.debug",
                # Menambahkan objek request ke konteks template.
                "django.template.context_processors.request",
                # Menambahkan data otentikasi (misalnya user) ke konteks.
                "django.contrib.auth.context_processors.auth",
                # Menambahkan pesan sementara ke konteks template.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Menentukan aplikasi WSGI untuk menjalankan proyek di server web.
WSGI_APPLICATION = "django_project.wsgi.application"

# Konfigurasi database.
# Menggunakan SQLite sebagai database default untuk pengembangan.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Backend SQLite.
        "NAME": BASE_DIR / "db.sqlite3",  # Lokasi file database.
    }
}

# Konfigurasi validasi kata sandi untuk memastikan keamanan.
AUTH_PASSWORD_VALIDATORS = [
    # Memeriksa kemiripan kata sandi dengan atribut pengguna (misalnya nama).
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    # Memeriksa panjang minimum kata sandi.
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # Memeriksa apakah kata sandi termasuk dalam daftar kata sandi umum.
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    # Memeriksa apakah kata sandi hanya berisi angka.
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Konfigurasi internasionalisasi untuk mendukung bahasa dan zona waktu.
LANGUAGE_CODE = "en-us"  # Bahasa default adalah Inggris (US).
TIME_ZONE = "Asia/Jakarta"  # Zona waktu diatur ke Jakarta, Indonesia.
USE_I18N = True  # Mengaktifkan internasionalisasi (terjemahan).
USE_TZ = True  # Mengaktifkan dukungan zona waktu.

# Konfigurasi file statis (CSS, JavaScript, gambar statis).
STATIC_URL = "static/"  # URL untuk mengakses file statis (misalnya /static/css/style.css).
STATICFILES_DIRS = [BASE_DIR / "static"]  # Direktori tambahan untuk file statis.
STATIC_ROOT = BASE_DIR / "staticfiles"  # Direktori untuk mengumpulkan file statis saat produksi.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # Penyimpanan file statis default.

# Konfigurasi file media (file yang diunggah pengguna, seperti gambar menu).
MEDIA_URL = "/media/"  # URL untuk mengakses file media (misalnya /media/menu_images/item.jpg).
MEDIA_ROOT = BASE_DIR / "media"  # Direktori untuk menyimpan file media.

# Menentukan tipe field primary key default untuk model baru.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Menentukan model pengguna kustom untuk otentikasi.
AUTH_USER_MODEL = "accounts.CustomUser"  # Menggunakan model CustomUser dari aplikasi accounts.

# Konfigurasi django-allauth untuk otentikasi dan manajemen akun.
LOGIN_REDIRECT_URL = "home"  # URL tujuan setelah login berhasil.
ACCOUNT_LOGOUT_REDIRECT = "home"  # URL tujuan setelah logout.
SITE_ID = 1  # ID situs untuk django.contrib.sites (diperlukan oleh allauth).

# Backend otentikasi yang digunakan.
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Backend bawaan Django.
    "allauth.account.auth_backends.AuthenticationBackend",  # Backend django-allauth.
)

# Backend email untuk pengembangan (mencetak email ke konsol, bukan mengirimnya).
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Pengaturan tambahan untuk django-allauth.
ACCOUNT_SESSION_REMEMBER = True  # Mengingat sesi login pengguna secara default.
ACCOUNT_UNIQUE_EMAIL = True  # Memastikan alamat email unik untuk setiap akun.

# Konfigurasi metode login dan kolom pendaftaran (versi modern allauth v0.50.0+).
ACCOUNT_LOGIN_METHODS = {"email"}  # Hanya izinkan login menggunakan email.
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]  # Kolom wajib saat pendaftaran (email dan kata sandi).