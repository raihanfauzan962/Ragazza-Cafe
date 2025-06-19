# Impor modul settings dari django.conf untuk mengakses pengaturan proyek (misalnya DEBUG, MEDIA_URL).
from django.conf import settings
# Impor fungsi static dari django.conf.urls.static untuk melayani file media selama pengembangan.
from django.conf.urls.static import static
# Impor modul admin dari django.contrib untuk mengaktifkan antarmuka admin Django.
from django.contrib import admin
# Impor fungsi path dan include dari django.urls untuk mendefinisikan pola URL dan menyertakan URL dari aplikasi lain.
from django.urls import path, include

# Mendefinisikan daftar pola URL menggunakan variabel urlpatterns.
urlpatterns = [
    # URL untuk mengakses antarmuka admin Django (misalnya: /admin/).
    # Memetakan ke admin.site.urls yang menyediakan fungsi admin bawaan.
    path("admin/", admin.site.urls),
    
    # URL untuk manajemen pengguna melalui django-allauth (misalnya: /accounts/login/, /accounts/signup/).
    # Menggunakan include("allauth.urls") untuk menyertakan semua URL yang disediakan oleh django-allauth.
    path("accounts/", include("allauth.urls")),
    
    # URL untuk aplikasi lokal 'pages' (misalnya: halaman beranda atau halaman statis).
    # Menggunakan include("pages.urls") untuk menyertakan pola URL dari aplikasi pages.
    # URL root (/) diarahkan ke aplikasi ini.
    path("", include("pages.urls")),
    
    # URL untuk aplikasi lokal 'cafe' (misalnya: /cafe/, /cafe/menu/, /cafe/checkout/).
    # Menggunakan include("cafe.urls") untuk menyertakan pola URL dari aplikasi cafe.
    path("cafe/", include("cafe.urls")),
]

# Jika pengaturan DEBUG di settings.py bernilai True (mode pengembangan).
if settings.DEBUG:
    # Tambahkan pola URL untuk melayani file media (misalnya: gambar yang diunggah).
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) memetakan URL media ke direktori media.
    # Contoh: /media/menu_images/item.jpg akan mengakses file di direktori MEDIA_ROOT.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)