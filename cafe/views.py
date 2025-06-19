# Impor fungsi render untuk merender template HTML, get_object_or_404 untuk mengambil objek atau menampilkan 404, dan redirect untuk pengalihan URL.
from django.shortcuts import render, get_object_or_404, redirect
# Impor login_required untuk membatasi akses ke pengguna yang sudah login.
from django.contrib.auth.decorators import login_required
# Impor messages untuk menampilkan pesan sementara (success, error, info) kepada pengguna.
from django.contrib import messages
# Impor semua model yang diperlukan dari file models.py untuk mengelola data.
from .models import Category, MenuItem, Order, OrderItem, Favorite, Review, Table, Reservation
# Impor form yang digunakan untuk input pengguna (CheckoutForm, ReviewForm, ReservationForm).
from .forms import CheckoutForm, ReviewForm, ReservationForm
# Impor Decimal untuk perhitungan finansial yang akurat (misalnya diskon).
from decimal import Decimal
# Impor timezone untuk menangani waktu berbasis zona waktu.
from django.utils import timezone
# Impor Sum untuk menghitung jumlah agregat dalam query database.
from django.db.models import Sum

# Fungsi pembantu untuk mendapatkan keranjang belanja dari session pengguna.
def get_cart(request):
    # Mengambil data keranjang dari session, jika tidak ada, kembalikan dictionary kosong.
    return request.session.get("cart", {})

# Fungsi pembantu untuk menyimpan keranjang belanja ke session.
def save_cart(request, cart):
    # Menyimpan keranjang ke session.
    request.session["cart"] = cart
    # Menandai session sebagai dimodifikasi agar perubahan tersimpan.
    request.session.modified = True

# View untuk menampilkan daftar menu.
def menu_list(request):
    # Mengambil semua kategori dari database.
    categories = Category.objects.all()
    # Mendapatkan parameter kategori yang dipilih dari query string (misalnya ?category=Makanan).
    selected_category = request.GET.get("category")
    # Mengambil item menu yang memiliki stok lebih dari 0.
    menu_items = MenuItem.objects.filter(stock__gt=0)
    # Jika kategori dipilih, filter item menu berdasarkan kategori tersebut.
    if selected_category:
        menu_items = menu_items.filter(category__name=selected_category)

    # Inisialisasi daftar rekomendasi kosong.
    recommendations = []
    # Jika pengguna sudah login, buat rekomendasi berdasarkan riwayat pesanan.
    if request.user.is_authenticated:
        # Mengambil 3 item menu yang paling sering dipesan oleh pengguna.
        ordered_items = (OrderItem.objects
                         .filter(order__user=request.user)  # Filter berdasarkan pengguna.
                         .values('menu_item')  # Ambil ID item menu.
                         .annotate(total=Sum('quantity'))  # Hitung total kuantitas per item.
                         .order_by('-total')[:3])  # Urutkan dari terbanyak dan ambil 3 teratas.

        # Ambil ID item menu dari hasil query.
        menu_ids = [entry['menu_item'] for entry in ordered_items]
        # Ambil objek MenuItem berdasarkan ID untuk rekomendasi.
        recommendations = MenuItem.objects.filter(id__in=menu_ids)

    # Merender template menu_list.html dengan data kategori, item menu, kategori terpilih, dan rekomendasi.
    return render(request, "cafe/menu_list.html", {
        "categories": categories,
        "menu_items": menu_items,
        "selected_category": selected_category,
        "recommendations": recommendations,
    })

# View untuk menampilkan detail item menu.
def menu_detail(request, pk):
    # Mengambil item menu berdasarkan ID (pk), atau menampilkan 404 jika tidak ditemukan.
    item = get_object_or_404(MenuItem, pk=pk)
    # Mengambil semua ulasan untuk item menu tersebut.
    reviews = Review.objects.filter(menu_item=item)
    # Membuat instance form untuk menambahkan ulasan baru.
    review_form = ReviewForm()
    # Merender template menu_detail.html dengan data item, ulasan, dan form ulasan.
    return render(request, "cafe/menu_detail.html", {
        "item": item,
        "reviews": reviews,
        "review_form": review_form,
    })

# View untuk menambahkan item ke keranjang belanja, memerlukan login.
@login_required
def add_to_cart(request, pk):
    # Mengambil item menu berdasarkan ID, atau menampilkan 404 jika tidak ditemukan.
    item = get_object_or_404(MenuItem, pk=pk)
    # Mengambil keranjang belanja dari session.
    cart = get_cart(request)
    # Mengubah ID item menjadi string untuk digunakan sebagai kunci di keranjang.
    item_id = str(item.id)
    # Menambah kuantitas item di keranjang (default 0 jika belum ada, tambah 1).
    cart[item_id] = cart.get(item_id, 0) + 1
    # Menyimpan keranjang yang diperbarui ke session.
    save_cart(request, cart)
    # Menampilkan pesan sukses bahwa item telah ditambahkan.
    messages.success(request, f"{item.name} ditambahkan ke keranjang.")
    # Mengalihkan kembali ke halaman detail menu.
    return redirect("menu_detail", pk=pk)

# View untuk menampilkan isi keranjang belanja, memerlukan login.
@login_required
def cart_view(request):
    # Mengambil keranjang belanja dari session.
    cart = get_cart(request)
    # Inisialisasi daftar item dan total harga.
    items = []
    total = 0

    # Iterasi setiap item di keranjang.
    for item_id, quantity in cart.items():
        # Mengambil item menu berdasarkan ID.
        item = get_object_or_404(MenuItem, pk=item_id)
        # Menghitung subtotal (harga x kuantitas).
        subtotal = item.price * quantity

        # Inisialisasi diskon sebagai 0.
        discount = Decimal(0)
        # Jika kuantitas >= 3, berikan diskon 10% dari subtotal.
        if quantity >= 3:
            discount = subtotal * Decimal(0.10)  # 10% diskon

        # Hitung subtotal setelah diskon.
        subtotal_after_discount = subtotal - discount

        # Tambahkan data item ke daftar untuk ditampilkan.
        items.append({
            "item": item,
            "quantity": quantity,
            "subtotal": subtotal,  # Harga sebelum diskon.
            "discount": discount,
            "subtotal_after_discount": subtotal_after_discount,
        })
        # Tambahkan subtotal setelah diskon ke total.
        total += subtotal_after_discount

    # Merender template cart.html dengan daftar item dan total harga.
    return render(request, "cafe/cart.html", {
        "items": items,
        "total": total,
    })

# View untuk proses checkout, memerlukan login.
@login_required
def checkout(request):
    # Mengambil keranjang belanja dari session.
    cart = get_cart(request)
    # Jika keranjang kosong, tampilkan pesan error dan alihkan ke daftar menu.
    if not cart:
        messages.error(request, "Keranjang kosong.")
        return redirect("menu_list")

    # Jika metode request adalah POST (form disubmit).
    if request.method == "POST":
        # Membuat instance form dengan data POST.
        form = CheckoutForm(request.POST)
        # Jika form valid, proses pembuatan pesanan.
        if form.is_valid():
            # Membuat objek Order baru dengan data dari form.
            order = Order.objects.create(
                user=request.user,
                table_number=form.cleaned_data["table"].table_number,
                payment_method=form.cleaned_data["payment_method"],
                note=form.cleaned_data.get('note', ''),
                created_at=timezone.now(),
            )
            # Iterasi setiap item di keranjang untuk membuat OrderItem.
            for item_id, quantity in cart.items():
                # Mengambil item menu berdasarkan ID.
                item = get_object_or_404(MenuItem, pk=item_id)
                # Membuat objek OrderItem untuk setiap item di keranjang.
                OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
                # Kurangi stok item sesuai kuantitas yang dipesan.
                item.stock -= quantity
                
                # Jika stok < 2, tambah stok otomatis sebanyak 10.
                if item.stock < 2:
                    item.stock += 10
                    messages.info(request, f"Stok {item.name} menipis, otomatis ditambah 10.")
                # Simpan perubahan stok ke database.
                item.save()
            # Kosongkan keranjang setelah pesanan dibuat.
            save_cart(request, {})
            # Tampilkan pesan sukses.
            messages.success(request, "Pesanan berhasil dibuat.")
            # Alihkan ke halaman detail pesanan.
            return redirect("order_detail", pk=order.pk)
    else:
        # Jika bukan POST, buat form kosong.
        form = CheckoutForm()
        # Atur queryset untuk field table agar menampilkan semua meja.
        form.fields["table"].queryset = Table.objects.all()

    # Merender template checkout.html dengan form checkout.
    return render(request, "cafe/checkout.html", {"form": form})

# View untuk menampilkan daftar pesanan pengguna, memerlukan login.
@login_required
def order_list(request):
    # Mengambil semua pesanan milik pengguna, diurutkan dari terbaru.
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # Merender template order_list.html dengan daftar pesanan.
    return render(request, 'cafe/order_list.html', {'orders': orders})

# View untuk menampilkan detail pesanan, memerlukan login.
@login_required
def order_detail(request, pk):
    # Mengambil pesanan berdasarkan ID dan pengguna, atau menampilkan 404.
    order = get_object_or_404(Order, pk=pk, user=request.user)
    # Merender template order_detail.html dengan data pesanan.
    return render(request, "cafe/order_detail.html", {"order": order})

# View untuk menampilkan daftar favorit pengguna, memerlukan login.
@login_required
def favorites_list(request):
    # Mengambil semua item favorit milik pengguna.
    favorites = Favorite.objects.filter(user=request.user)
    # Merender template favorites.html dengan daftar favorit.
    return render(request, "cafe/favorites.html", {"favorites": favorites})

# View untuk menambahkan item ke favorit, memerlukan login.
@login_required
def add_to_favorites(request, pk):
    # Mengambil item menu berdasarkan ID, atau menampilkan 404.
    item = get_object_or_404(MenuItem, pk=pk)
    # Membuat objek Favorite jika belum ada (menggunakan get_or_create untuk menghindari duplikat).
    Favorite.objects.get_or_create(user=request.user, menu_item=item)
    # Tampilkan pesan sukses.
    messages.success(request, f"{item.name} ditambahkan ke favorit.")
    # Alihkan kembali ke halaman detail menu.
    return redirect("menu_detail", pk=pk)

# View untuk menambahkan ulasan untuk item menu, memerlukan login.
@login_required
def add_review(request, pk):
    # Mengambil item menu berdasarkan ID, atau menampilkan 404.
    item = get_object_or_404(MenuItem, pk=pk)
    # Jika metode request adalah POST (form disubmit).
    if request.method == "POST":
        # Membuat instance form dengan data POST.
        form = ReviewForm(request.POST)
        # Jika form valid, buat ulasan baru.
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                menu_item=item,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"]
            )
            # Tampilkan pesan sukses.
            messages.success(request, "Review ditambahkan.")
    # Alihkan kembali ke halaman detail menu (baik POST maupun GET).
    return redirect("menu_detail", pk=pk)

# View untuk mengelola reservasi meja, memerlukan login.
@login_required
def reservation_view(request):
    # Mengambil semua reservasi milik pengguna, diurutkan dari terbaru.
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    # Membuat instance form reservasi kosong.
    form = ReservationForm()

    # Jika metode request adalah POST (form disubmit).
    if request.method == "POST":
        # Membuat instance form dengan data POST.
        form = ReservationForm(request.POST)
        # Jika form valid, proses pembuatan reservasi.
        if form.is_valid():
            # Ambil data dari form.
            table = form.cleaned_data['table']
            date = form.cleaned_data['reservation_date']
            time = form.cleaned_data['reservation_time']

            # Cek apakah meja sudah dipesan pada tanggal dan waktu yang sama.
            exists = Reservation.objects.filter(
                table=table,
                reservation_date=date,
                reservation_time=time
            ).exists()

            # Jika sudah ada reservasi, tampilkan pesan error.
            if exists:
                messages.error(request, f"Meja {table} sudah dibooking di waktu tersebut.")
            else:
                # Buat reservasi baru jika meja tersedia.
                Reservation.objects.create(
                    user=request.user,
                    table=table,
                    reservation_date=date,
                    reservation_time=time,
                    note=form.cleaned_data.get('note', '')
                )
                # Tampilkan pesan sukses.
                messages.success(request, f"Reservasi untuk Meja {table} berhasil dibuat.")
                # Alihkan ke halaman reservasi untuk mereset form.
                return redirect("reservation")

    # Merender template reservation.html dengan form dan daftar reservasi.
    return render(request, "cafe/reservation.html", {
        "form": form,
        "reservations": reservations
    })