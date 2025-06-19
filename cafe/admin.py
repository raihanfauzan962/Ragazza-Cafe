# Impor modul admin dari django.contrib untuk mengelola antarmuka admin Django.
from django.contrib import admin
# Impor HttpResponse untuk membuat respons HTTP, seperti mengunduh file PDF.
from django.http import HttpResponse
# Impor format_html untuk membuat HTML yang aman dari serangan XSS di admin.
from django.utils.html import format_html
# Impor semua model (Category, MenuItem, dll.) dari file models.py untuk didaftarkan ke admin.
from .models import Category, MenuItem, Order, OrderItem, Favorite, Review, Table, Reservation 
# Impor colors dari reportlab.lib untuk mengatur warna pada tabel di PDF.
from reportlab.lib import colors
# Impor inch dari reportlab.lib.units untuk menentukan ukuran dalam satuan inci.
from reportlab.lib.units import inch
# Impor komponen ReportLab untuk membuat dokumen PDF, seperti tabel, paragraf, dan dokumen sederhana.
from reportlab.platypus import SimpleDocTemplate, Table as RLTable, TableStyle, Paragraph, Spacer
# Impor gaya teks sampel dari ReportLab untuk formatting teks di PDF.
from reportlab.lib.styles import getSampleStyleSheet
# Impor datetime untuk menangani format tanggal dan waktu di laporan.
from datetime import datetime
# Impor io untuk menangani buffer memori sementara saat membuat PDF.
import io
# Impor qrcode untuk menghasilkan kode QR untuk nomor meja.
import qrcode
# Impor BytesIO untuk menyimpan gambar QR code dalam memori sebagai byte.
from io import BytesIO
# Impor base64 untuk mengkodekan gambar QR code menjadi format base64 agar bisa ditampilkan di HTML.
import base64

# Membuat kelas OrderItemInline untuk menampilkan OrderItem sebagai tabel di dalam form Order di admin.
class OrderItemInline(admin.TabularInline):
    # Menentukan model yang digunakan adalah OrderItem.
    model = OrderItem
    # Tidak menambahkan baris kosong ekstra untuk input baru di form.
    extra = 0
    # Kolom menu_item dan quantity hanya dapat dilihat, tidak dapat diedit di admin.
    readonly_fields = ('menu_item', 'quantity')

# Membuat kelas OrderAdmin untuk mengatur tampilan dan fungsi model Order di antarmuka admin.
class OrderAdmin(admin.ModelAdmin):
    # Menentukan kolom yang ditampilkan di daftar Order di admin: ID, pengguna, nomor meja, dll.
    list_display = ['id', 'user', 'table_number', 'created_at', 'order_status', 'payment_status', 'payment_method']
    # Menambahkan filter di sidebar untuk memfilter berdasarkan status pesanan, pembayaran, dll.
    list_filter = ['order_status', 'payment_status', 'payment_method', 'created_at']
    # Menambahkan fungsi pencarian berdasarkan nama pengguna dan nomor meja.
    search_fields = ['user__username', 'table_number']
    # Menyertakan OrderItemInline untuk menampilkan item pesanan di bawah setiap pesanan.
    inlines = [OrderItemInline]

    # Metode untuk mengatur gaya tabel PDF yang digunakan di invoice dan laporan penjualan.
    def _get_table_style(self):
        # Mengembalikan TableStyle dengan pengaturan warna, font, dan tata letak.
        return TableStyle([
            # Latar belakang baris header berwarna cokelat.
            ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
            # Warna teks header putih asap (whitesmoke).
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            # Semua teks di tabel rata tengah.
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # Font header adalah Helvetica-Bold.
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            # Ukuran font header adalah 12.
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            # Jarak bawah header lebih besar untuk estetika.
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Latar belakang baris data berwarna krem (beige).
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            # Menambahkan garis grid hitam di seluruh tabel.
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

    # Metode untuk menghasilkan invoice PDF untuk pesanan yang dipilih di admin.
    def generate_invoice_pdf(self, request, queryset):
        # Membuat respons HTTP dengan tipe konten PDF.
        response = HttpResponse(content_type='application/pdf')
        # Menentukan nama file yang akan diunduh sebagai "invoice.pdf".
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        # Membuat buffer sementara di memori untuk menyimpan PDF.
        buffer = io.BytesIO()
        # Membuat dokumen PDF menggunakan SimpleDocTemplate.
        doc = SimpleDocTemplate(buffer)
        # Daftar elemen (paragraf, tabel, dll.) yang akan dimasukkan ke PDF.
        elements = []
        # Mendapatkan gaya teks standar dari ReportLab.
        styles = getSampleStyleSheet()

        # Iterasi setiap pesanan yang dipilih.
        for order in queryset:
            # Membuat data tabel: header dan item pesanan.
            data = [['Menu Item', 'Quantity', 'Price', 'Subtotal']]
            total = 0
            # Iterasi setiap item dalam pesanan.
            for item in order.items.all():
                # Menghitung subtotal per item (kuantitas * harga).
                subtotal = item.quantity * item.menu_item.price
                total += subtotal
                # Menambahkan data item ke tabel.
                data.append([item.menu_item.name, item.quantity, f"Rp{item.menu_item.price}", f"Rp{subtotal}"])
            # Menambahkan baris total di tabel.
            data.append(['', '', 'Total', f"Rp{total}"])

            # Membuat tabel PDF dengan lebar kolom yang ditentukan.
            table = RLTable(data, colWidths=[2*inch, 1*inch, 1.5*inch, 1.5*inch])
            # Mengatur gaya tabel menggunakan metode _get_table_style.
            table.setStyle(self._get_table_style())

            # Menambahkan judul invoice dengan nomor pesanan.
            elements.append(Paragraph(f"Invoice for Order #{order.id}", styles['Heading1']))
            # Menambahkan informasi pelanggan.
            elements.append(Paragraph(f"Customer: {order.user.username}", styles['Normal']))
            # Menambahkan nomor meja.
            elements.append(Paragraph(f"Table: {order.table_number}", styles['Normal']))
            # Menambahkan tanggal dan waktu pesanan.
            elements.append(Paragraph(f"Date: {order.created_at.strftime('%d %B %Y %H:%M')}", styles['Normal']))
            # Menambahkan metode pembayaran.
            elements.append(Paragraph(f"Payment Method: {order.get_payment_method_display()}", styles['Normal']))
            # Menambahkan jarak antar elemen.
            elements.append(Spacer(1, 12))
            # Menambahkan tabel ke elemen PDF.
            elements.append(table)
            # Menambahkan jarak setelah tabel.
            elements.append(Spacer(1, 24))

        # Membangun dokumen PDF dari elemen-elemen yang telah ditambahkan.
        doc.build(elements)
        # Mengambil data PDF dari buffer.
        pdf = buffer.getvalue()
        # Menutup buffer untuk membersihkan memori.
        buffer.close()
        # Menulis data PDF ke respons HTTP.
        response.write(pdf)
        # Mengembalikan respons untuk mengunduh PDF.
        return response

    # Deskripsi singkat untuk aksi generate_invoice_pdf di admin.
    generate_invoice_pdf.short_description = "Generate Invoice PDF for selected orders"
    # Menambahkan aksi generate_invoice_pdf ke daftar aksi admin.
    actions = [generate_invoice_pdf]

    # Metode untuk menghasilkan laporan penjualan PDF berdasarkan pesanan yang dipilih.
    def generate_sales_report(self, request, queryset):
        # Membuat respons HTTP dengan tipe konten PDF.
        response = HttpResponse(content_type='application/pdf')
        # Menentukan nama file yang akan diunduh sebagai "sales_report.pdf".
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        # Membuat buffer sementara untuk menyimpan PDF.
        buffer = io.BytesIO()
        # Membuat dokumen PDF menggunakan SimpleDocTemplate.
        doc = SimpleDocTemplate(buffer)
        # Daftar elemen untuk PDF.
        elements = []
        # Mendapatkan gaya teks standar dari ReportLab.
        styles = getSampleStyleSheet()

        # Menambahkan judul laporan penjualan.
        elements.append(Paragraph("Sales Report", styles['Heading1']))
        # Menambahkan tanggal dan waktu pembuatan laporan.
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}", styles['Normal']))
        # Menambahkan jarak antar elemen.
        elements.append(Spacer(1, 12))

        # Menginisialisasi dictionary untuk menyimpan data penjualan per item.
        item_sales = {}
        # Menginisialisasi total penjualan keseluruhan.
        total_sales = 0

        # Iterasi setiap pesanan untuk mengumpulkan data penjualan.
        for order in queryset:
            order_total = 0
            # Iterasi setiap item dalam pesanan.
            for item in order.items.all():
                # Menghitung subtotal per item.
                subtotal = item.quantity * item.menu_item.price
                order_total += subtotal
                # Menginisialisasi data item jika belum ada di dictionary.
                if item.menu_item.name not in item_sales:
                    item_sales[item.menu_item.name] = {'quantity': 0, 'subtotal': 0}
                # Menambahkan kuantitas dan subtotal ke data item.
                item_sales[item.menu_item.name]['quantity'] += item.quantity
                item_sales[item.menu_item.name]['subtotal'] += subtotal
            # Menambahkan total pesanan ke total penjualan keseluruhan.
            total_sales += order_total

        # Membuat tabel ringkasan penjualan per item.
        item_data = [['Menu Item', 'Quantity Sold', 'Total']]
        # Mengisi tabel dengan data penjualan per item.
        for name, data in item_sales.items():
            item_data.append([name, data['quantity'], f"Rp{data['subtotal']}"])
        # Menambahkan baris total keseluruhan.
        item_data.append(['', 'Grand Total', f"Rp{total_sales}"])

        # Membuat tabel PDF untuk ringkasan penjualan item.
        item_table = RLTable(item_data, colWidths=[3*inch, 1.5*inch, 2*inch])
        # Mengatur gaya tabel.
        item_table.setStyle(self._get_table_style())

        # Menambahkan judul untuk ringkasan penjualan item.
        elements.append(Paragraph("Item Sales Summary", styles['Heading2']))
        # Menambahkan tabel ringkasan item.
        elements.append(item_table)
        # Menambahkan jarak setelah tabel.
        elements.append(Spacer(1, 24))

        # Membuat tabel ringkasan pesanan.
        order_data = [['Order ID', 'Table', 'Date', 'Total']]
        # Mengisi tabel dengan data setiap pesanan.
        for order in queryset:
            # Menghitung total pesanan.
            order_total = sum(item.quantity * item.menu_item.price for item in order.items.all())
            order_data.append([
                f"#{order.id}",
                order.table_number,
                order.created_at.strftime('%d %b %Y %H:%M'),
                f"Rp{order_total}"
            ])
        # Menambahkan baris total penjualan.
        order_data.append(['', '', 'Total Sales', f"Rp{total_sales}"])

        # Membuat tabel PDF untuk ringkasan pesanan.
        order_table = RLTable(order_data, colWidths=[1*inch, 1*inch, 2.5*inch, 2*inch])
        # Mengatur gaya tabel.
        order_table.setStyle(self._get_table_style())

        # Menambahkan judul untuk ringkasan pesanan.
        elements.append(Paragraph("Order Summary", styles['Heading2']))
        # Menambahkan tabel ringkasan pesanan.
        elements.append(order_table)

        # Membangun dokumen PDF dari elemen-elemen.
        doc.build(elements)

        # Mengambil data PDF dari buffer.
        pdf = buffer.getvalue()
        # Menutup buffer.
        buffer.close()
        # Menulis data PDF ke respons HTTP.
        response.write(pdf)
        # Mengembalikan respons untuk mengunduh PDF.
        return response

    # Deskripsi singkat untuk aksi generate_sales_report di admin.
    generate_sales_report.short_description = "Generate Sales Report PDF"
    # Menambahkan aksi generate_sales_report ke daftar aksi admin.
    actions.append(generate_sales_report)

# Membuat kelas TableAdmin untuk mengatur tampilan dan fungsi model Table di admin.
class TableAdmin(admin.ModelAdmin):
    # Menentukan kolom yang ditampilkan: nomor meja dan tautan unduh QR code.
    list_display = ['table_number', 'qr_code_download']

    # Metode untuk menghasilkan dan menampilkan QR code serta tautan unduhnya.
    def qr_code_download(self, obj):
        # Membuat objek QR code dengan pengaturan dasar.
        qr = qrcode.QRCode(
            version=1,  # Versi QR code (ukuran dan kapasitas data).
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Tingkat koreksi kesalahan rendah.
            box_size=10,  # Ukuran kotak dalam piksel.
            border=4,  # Lebar border dalam kotak.
        )
        # Menentukan URL lokal untuk meja (contoh: http://127.0.0.1:8000/table/1/).
        url = f"http://127.0.0.1:8000/table/{obj.table_number}/"
        # Menambahkan URL ke data QR code.
        qr.add_data(url)
        # Membuat QR code agar sesuai dengan data.
        qr.make(fit=True)
        # Membuat gambar QR code dengan warna hitam dan latar belakang putih.
        img = qr.make_image(fill_color="black", back_color="white")

        # Menyimpan gambar QR code ke buffer memori.
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_data = buffer.getvalue()
        buffer.close()

        # Mengkodekan gambar ke format base64 untuk ditampilkan di HTML.
        base64_img = base64.b64encode(img_data).decode('utf-8')

        # Mengembalikan HTML yang berisi tautan unduh dan gambar QR code.
        return format_html(
            '<a download="table_{}.png" href="data:image/png;base64,{}">Download QR</a><br>'
            '<img src="data:image/png;base64,{}" width="100"/>',
            obj.table_number, base64_img, base64_img
        )

    # Deskripsi singkat untuk kolom qr_code_download di admin.
    qr_code_download.short_description = 'QR Code'

# Membuat kelas ReservationAdmin untuk mengatur tampilan model Reservation di admin.
class ReservationAdmin(admin.ModelAdmin):
    # Menentukan kolom yang ditampilkan: ID, pengguna, meja, tanggal reservasi, dll.
    list_display = ['id', 'user', 'table', 'reservation_date', 'reservation_time', 'created_at']
    # Menambahkan filter berdasarkan tanggal dan waktu reservasi.
    list_filter = ['reservation_date', 'reservation_time']
    # Menambahkan fungsi pencarian berdasarkan nama pengguna dan nomor meja.
    search_fields = ['user__username', 'table__table_number']
    # Mengurutkan daftar berdasarkan tanggal dan waktu reservasi, terbaru dulu.
    ordering = ['-reservation_date', '-reservation_time']

# Mendaftarkan model Category ke admin dengan pengaturan default.
admin.site.register(Category)
# Mendaftarkan model MenuItem ke admin dengan pengaturan default.
admin.site.register(MenuItem)
# Mendaftarkan model Order dengan kelas OrderAdmin untuk pengaturan khusus.
admin.site.register(Order, OrderAdmin)
# Mendaftarkan model OrderItem ke admin dengan pengaturan default.
admin.site.register(OrderItem)
# Mendaftar model Favorite ke admin dengan pengaturan default.
admin.site.register(Favorite)
# Mendaftar model Review ke admin dengan pengaturan default.
admin.site.register(Review)
# Mendaftar model Table dengan kelas TableAdmin untuk pengaturan khusus.
admin.site.register(Table, TableAdmin)
# Mendaftar model Reservation dengan kelas ReservationAdmin untuk pengaturan khusus.
admin.site.register(Reservation, ReservationAdmin)