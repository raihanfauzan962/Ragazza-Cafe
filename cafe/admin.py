from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Favorite, Review
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['price', 'stock']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

def export_invoice(modeladmin, request, queryset):
    if queryset.count() != 1:
        return HttpResponse("Pilih satu pesanan saja untuk mencetak invoice.", status=400)

    order = queryset.first()
    items = order.items.all()
    total = sum([item.get_total_price() for item in items])

    context = {
        'order': order,
        'items': items,
        'total': total,
        'generated_at': datetime.datetime.now()
    }

    html = render_to_string('admin/invoice.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

export_invoice.short_description = "Export Invoice to PDF"


def export_sales_report(modeladmin, request, queryset):
    items = {}
    total_profit = 0

    for order in queryset.filter(order_status='done'):
        for item in order.items.all():
            name = item.menu_item.name
            subtotal = item.get_total_price()
            if name not in items:
                items[name] = {'quantity': 0, 'subtotal': 0}
            items[name]['quantity'] += item.quantity
            items[name]['subtotal'] += subtotal
            total_profit += subtotal

    context = {
        'items': items,
        'total_profit': total_profit,
        'generated_at': datetime.datetime.now()
    }

    html = render_to_string('admin/sales_report.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

export_sales_report.short_description = "Export Sales Report to PDF"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'table_number', 'payment_method', 'payment_status', 'order_status', 'note', 'created_at']
    list_filter = ['payment_status', 'order_status', 'created_at']
    search_fields = ['user__email']
    inlines = [OrderItemInline]
    actions = [export_sales_report, export_invoice]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['menu_item__name', 'user__email']



