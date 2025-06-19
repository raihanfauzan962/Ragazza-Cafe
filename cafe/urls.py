# Impor fungsi path dari django.urls untuk mendefinisikan pola URL.
from django.urls import path
# Impor modul views dari direktori saat ini (file views.py) untuk menghubungkan URL dengan fungsi view.
from . import views

# Mendefinisikan daftar pola URL menggunakan variabel urlpatterns.
urlpatterns = [
    # URL untuk halaman daftar menu (root URL, misalnya: /).
    # Memetakan URL kosong ke fungsi views.menu_list.
    # Nama 'menu_list' digunakan untuk referensi URL di template atau kode lain.
    path("", views.menu_list, name="menu_list"),
    
    # URL untuk halaman detail menu berdasarkan ID item menu (primary key).
    # Pola <int:pk> menangkap ID sebagai bilangan bulat dan mengirimkannya ke view sebagai parameter.
    # Memetakan ke fungsi views.menu_detail.
    # Nama 'menu_detail' digunakan untuk referensi URL.
    path("menu/<int:pk>/", views.menu_detail, name="menu_detail"),
    
    # URL untuk menambahkan item menu ke keranjang belanja berdasarkan ID item.
    # Pola <int:pk> menangkap ID item menu.
    # Memetakan ke fungsi views.add_to_cart.
    # Nama 'add_to_cart' digunakan untuk referensi URL.
    path("menu/<int:pk>/add/", views.add_to_cart, name="add_to_cart"),
    
    # URL untuk halaman keranjang belanja.
    # Memetakan ke fungsi views.cart_view.
    # Nama 'cart' digunakan untuk referensi URL.
    path("cart/", views.cart_view, name="cart"),
    
    # URL untuk halaman checkout (pembayaran pesanan).
    # Memetakan ke fungsi views.checkout.
    # Nama 'checkout' digunakan untuk referensi URL.
    path("checkout/", views.checkout, name="checkout"),
    
    # URL untuk halaman daftar pesanan pengguna.
    # Memetakan ke fungsi views.order_list.
    # Nama 'order_list' digunakan untuk referensi URL.
    path("order/", views.order_list, name="order_list"),
    
    # URL untuk halaman detail pesanan berdasarkan ID pesanan.
    # Pola <int:pk> menangkap ID pesanan.
    # Memetakan ke fungsi views.order_detail.
    # Nama 'order_detail' digunakan untuk referensi URL.
    path("order/<int:pk>/", views.order_detail, name="order_detail"),
    
    # URL untuk halaman daftar item favorit pengguna.
    # Memetakan ke fungsi views.favorites_list.
    # Nama 'favorites' digunakan untuk referensi URL.
    path("favorites/", views.favorites_list, name="favorites"),
    
    # URL untuk menambahkan item menu ke daftar favorit berdasarkan ID item.
    # Pola <int:pk> menangkap ID item menu.
    # Memetakan ke fungsi views.add_to_favorites.
    # Nama 'add_to_favorites' digunakan untuk referensi URL.
    path("menu/<int:pk>/favorite/", views.add_to_favorites, name="add_to_favorites"),
    
    # URL untuk menambahkan ulasan untuk item menu berdasarkan ID item.
    # Pola <int:pk> menangkap ID item menu.
    # Memetakan ke fungsi views.add_review.
    # Nama 'add_review' digunakan untuk referensi URL.
    path("menu/<int:pk>/review/", views.add_review, name="add_review"),
    
    # URL untuk halaman reservasi meja.
    # Memetakan ke fungsi views.reservation_view.
    # Nama 'reservation' digunakan untuk referensi URL.
    path("reservation/", views.reservation_view, name="reservation"),
]