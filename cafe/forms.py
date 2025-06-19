# Impor modul forms dari Django untuk membuat form berbasis model dan form biasa.
from django import forms
# Impor model Review, Reservation, dan Table dari file models.py untuk digunakan dalam form.
from .models import Review, Reservation, Table

# Membuat kelas CheckoutForm sebagai form biasa (bukan berbasis model) untuk proses checkout.
class CheckoutForm(forms.Form):
    # Membuat field untuk memilih nomor meja dari model Table.
    table = forms.ModelChoiceField(
        # Mengambil semua objek Table dari database sebagai opsi pilihan.
        queryset=Table.objects.all(),
        # Label yang ditampilkan di form untuk field ini.
        label="Nomor Meja",
        # Menggunakan widget Select (dropdown) dengan kelas CSS 'form-control' untuk styling.
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Membuat field untuk memilih metode pembayaran.
    payment_method = forms.ChoiceField(
        # Pilihan metode pembayaran: tunai atau non-tunai.
        choices=[
            ('cash', 'Tunai'),
            ('non-cash', 'Non-Tunai'),
        ],
        # Label yang ditampilkan di form untuk field ini.
        label="Metode Pembayaran",
        # Menggunakan widget Select (dropdown) dengan kelas CSS 'form-control' untuk styling.
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Membuat field untuk catatan tambahan (opsional).
    note = forms.CharField(
        # Field ini tidak wajib diisi (opsional).
        required=False,
        # Label yang ditampilkan di form untuk field ini.
        label="Catatan",
        # Menggunakan widget Textarea dengan 3 baris dan placeholder untuk petunjuk pengguna.
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tambahkan catatan khusus (opsional)...'})
    )

# Membuat kelas ReviewForm sebagai form berbasis model untuk mengelola ulasan (review).
class ReviewForm(forms.ModelForm):
    # Kelas Meta untuk mengatur konfigurasi form berbasis model.
    class Meta:
        # Menentukan model yang digunakan adalah Review.
        model = Review
        # Menentukan field yang akan dimasukkan ke form: rating dan comment.
        fields = ['rating', 'comment']

# Impor model Reservation (meskipun sudah diimpor di atas, ini mungkin redundan tetapi tidak memengaruhi fungsi).
from .models import Reservation

# Membuat kelas ReservationForm sebagai form berbasis model untuk mengelola reservasi.
class ReservationForm(forms.ModelForm):
    # Kelas Meta untuk mengatur konfigurasi form berbasis model.
    class Meta:
        # Menentukan model yang digunakan adalah Reservation.
        model = Reservation
        # Menentukan field yang akan dimasukkan ke form: meja, tanggal reservasi, waktu reservasi, dan catatan.
        fields = ['table', 'reservation_date', 'reservation_time', 'note']
        # Mengatur widget untuk setiap field agar sesuai dengan kebutuhan input pengguna.
        widgets = {
            # Field reservation_date menggunakan input tipe date (HTML5 date picker).
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            # Field reservation_time menggunakan input tipe time (HTML5 time picker).
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
            # Field note menggunakan Textarea dengan 2 baris untuk input teks panjang.
            'note': forms.Textarea(attrs={'rows': 2}),
        }