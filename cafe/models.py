# Impor modul models dari Django untuk mendefinisikan model database.
from django.db import models
# Impor get_user_model untuk mendapatkan model pengguna kustom atau bawaan Django.
from django.contrib.auth import get_user_model

# Mendapatkan model pengguna yang aktif (bisa model bawaan Django atau model kustom).
User = get_user_model()

# Mendefinisikan model Category untuk kategori menu (misalnya: Makanan, Minuman).
class Category(models.Model):
    # Field untuk nama kategori dengan panjang maksimum 100 karakter.
    name = models.CharField(max_length=100)
    
    # Metode __str__ untuk menampilkan representasi string dari objek kategori (nama kategori).
    def __str__(self):
        return self.name

# Mendefinisikan model MenuItem untuk item menu restoran.
class MenuItem(models.Model):
    # Field untuk nama item menu dengan panjang maksimum 100 karakter.
    name = models.CharField(max_length=100)
    # Field untuk deskripsi item menu (teks panjang, misalnya bahan atau informasi tambahan).
    description = models.TextField()
    # Field untuk harga item menu dalam bentuk bilangan bulat (misalnya 15000 untuk Rp15.000).
    price = models.IntegerField()
    # Field untuk menghubungkan item menu dengan kategori (relasi ForeignKey).
    # Jika kategori dihapus, item menu terkait juga akan dihapus (on_delete=models.CASCADE).
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Field untuk gambar item menu, disimpan di folder 'menu_images/'.
    # Field ini opsional (blank=True, null=True).
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    # Field untuk stok item menu, default-nya adalah 0.
    stock = models.IntegerField(default=0)
    
    # Metode __str__ untuk menampilkan nama item menu sebagai representasi string.
    def __str__(self):
        return self.name

# Mendefinisikan model Order untuk pesanan pelanggan.
class Order(models.Model):
    # Pilihan untuk metode pembayaran: tunai atau non-tunai.
    PAYMENT_CHOICES = [
        ('cash', 'Tunai'),
        ('non-cash', 'Non-Tunai'),
    ]

    # Pilihan untuk status pesanan: menunggu, diproses, siap, atau selesai.
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('processing', 'Diproses'),
        ('ready', 'Siap Disajikan'),
        ('done', 'Selesai'),
    ]

    # Pilihan untuk status pembayaran: belum dibayar atau sudah dibayar.
    PAYMENT_STATUS = [
        ('unpaid', 'Belum Dibayar'),
        ('paid', 'Sudah Dibayar'),
    ]
    
    # Field untuk menghubungkan pesanan dengan pengguna yang membuatnya (ForeignKey ke User).
    # Jika pengguna dihapus, pesanan terkait juga dihapus (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field untuk menyimpan waktu pembuatan pesanan, otomatis diisi saat pesanan dibuat.
    created_at = models.DateTimeField(auto_now_add=True)
    # Field untuk nomor meja tempat pesanan dibuat (maksimum 10 karakter).
    table_number = models.CharField(max_length=10)
    # Field untuk metode pembayaran, menggunakan PAYMENT_CHOICES, default-nya 'cash'.
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    # Field untuk status pesanan, menggunakan STATUS_CHOICES, default-nya 'pending'.
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # Field untuk status pembayaran, menggunakan PAYMENT_STATUS, default-nya 'unpaid'.
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    # Field untuk catatan tambahan pesanan (opsional, boleh kosong).
    note = models.TextField(blank=True, null=True)
    
    # Metode __str__ untuk menampilkan representasi string pesanan (ID dan nama pengguna).
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Mendefinisikan model OrderItem untuk item individual dalam pesanan.
class OrderItem(models.Model):
    # Field untuk menghubungkan item pesanan dengan pesanan (ForeignKey ke Order).
    # related_name='items' memungkinkan akses ke semua item pesanan melalui order.items.
    # Jika pesanan dihapus, item terkait juga dihapus (on_delete=models.CASCADE).
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Field untuk menghubungkan item pesanan dengan item menu (ForeignKey ke MenuItem).
    # Jika item menu dihapus, item pesanan terkait juga dihapus (on_delete=models.CASCADE).
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # Field untuk jumlah item yang dipesan (harus bilangan bulat positif).
    quantity = models.PositiveIntegerField()
    
    # Metode __str__ untuk menampilkan jumlah dan nama item menu sebagai representasi string.
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

# Mendefinisikan model Favorite untuk menyimpan item menu favorit pengguna.
class Favorite(models.Model):
    # Field untuk menghubungkan favorit dengan pengguna (ForeignKey ke User).
    # Jika pengguna dihapus, favorit terkait juga dihapus (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field untuk menghubungkan favorit dengan item menu (ForeignKey ke MenuItem).
    # Jika item menu dihapus, favorit terkait juga dihapus (on_delete=models.CASCADE).
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    
    # Metode __str__ untuk menampilkan nama pengguna dan item menu favorit.
    def __str__(self):
        return f"{self.user.username}'s favorite: {self.menu_item.name}"

# Mendefinisikan model Review untuk ulasan pengguna terhadap item menu.
class Review(models.Model):
    # Field untuk menghubungkan ulasan dengan pengguna (ForeignKey ke User).
    # Jika pengguna dihapus, ulasan terkait juga dihapus (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field untuk menghubungkan ulasan dengan item menu (ForeignKey ke MenuItem).
    # Jika item menu dihapus, ulasan terkait juga dihapus (on_delete=models.CASCADE).
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # Field untuk rating (1 sampai 5), dibatasi dengan pilihan 1 hingga 5.
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    # Field untuk komentar ulasan (teks panjang).
    comment = models.TextField()
    # Field untuk waktu pembuatan ulasan, otomatis diisi saat ulasan dibuat.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metode __str__ untuk menampilkan nama pengguna dan item menu yang diulas.
    def __str__(self):
        return f"Review by {self.user.username} for {self.menu_item.name}"

# Mendefinisikan model Table untuk meja di restoran.
class Table(models.Model):
    # Field untuk nomor meja (maksimum 10 karakter, harus unik).
    table_number = models.CharField(max_length=10, unique=True)
    
    # Metode __str__ untuk menampilkan nomor meja sebagai representasi string.
    def __str__(self):
        return f"Meja {self.table_number}"

# Impor timezone dari django.utils untuk menangani waktu berbasis zona waktu.
from django.utils import timezone

# Mendefinisikan model Reservation untuk reservasi meja oleh pengguna.
class Reservation(models.Model):
    # Field untuk menghubungkan reservasi dengan pengguna (ForeignKey ke User).
    # Jika pengguna dihapus, reservasi terkait juga dihapus (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field untuk menghubungkan reservasi dengan meja (ForeignKey ke Table).
    # Jika meja dihapus, reservasi terkait juga dihapus (on_delete=models.CASCADE).
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    # Field untuk tanggal reservasi.
    reservation_date = models.DateField()
    # Field untuk waktu reservasi.
    reservation_time = models.TimeField()
    # Field untuk catatan tambahan reservasi (opsional, boleh kosong).
    note = models.TextField(blank=True, null=True)
    # Field untuk waktu pembuatan reservasi, otomatis diisi saat reservasi dibuat.
    created_at = models.DateTimeField(auto_now_add=True)

    # Metode __str__ untuk menampilkan detail reservasi (meja, pengguna, tanggal, waktu).
    def __str__(self):
        return f"Reservasi {self.table} oleh {self.user.username} pada {self.reservation_date} {self.reservation_time}"