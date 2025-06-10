from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, MenuItem, Order, OrderItem, Favorite, Review
from .forms import CheckoutForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# Helper untuk keranjang (gunakan session)
def get_cart(request):
    return request.session.get("cart", {})

def save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def menu_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get("category")
    menu_items = MenuItem.objects.filter(stock__gt=0)
    if selected_category:
        menu_items = menu_items.filter(category__name=selected_category)
    return render(request, "cafe/menu_list.html", {
        "categories": categories,
        "menu_items": menu_items,
        "selected_category": selected_category,
    })


def menu_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    reviews = Review.objects.filter(menu_item=item)
    review_form = ReviewForm()
    return render(request, "cafe/menu_detail.html", {
        "item": item,
        "reviews": reviews,
        "review_form": review_form,
    })


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    cart = get_cart(request)
    item_id = str(item.id)
    cart[item_id] = cart.get(item_id, 0) + 1
    save_cart(request, cart)
    messages.success(request, f"{item.name} ditambahkan ke keranjang.")
    return redirect("menu_detail", pk=pk)


@login_required
def cart_view(request):
    cart = get_cart(request)
    items = []
    total = 0
    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, pk=item_id)
        subtotal = item.price * quantity
        items.append({
            "item": item,
            "quantity": quantity,
            "subtotal": subtotal
        })
        total += subtotal
    return render(request, "cafe/cart.html", {"items": items, "total": total})


@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Keranjang kosong.")
        return redirect("menu_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                table_number=form.cleaned_data["table_number"],
                payment_method=form.cleaned_data["payment_method"],
                note=form.cleaned_data.get('note', ''),
                created_at=timezone.now(),
            )
            for item_id, quantity in cart.items():
                item = get_object_or_404(MenuItem, pk=item_id)
                OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
                item.stock -= quantity
                item.save()
            save_cart(request, {})
            messages.success(request, "Pesanan berhasil dibuat.")
            return redirect("order_detail", pk=order.pk)
    else:
        form = CheckoutForm()

    return render(request, "cafe/checkout.html", {"form": form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cafe/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "cafe/order_detail.html", {"order": order})


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, "cafe/favorites.html", {"favorites": favorites})


@login_required
def add_to_favorites(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    Favorite.objects.get_or_create(user=request.user, menu_item=item)
    messages.success(request, f"{item.name} ditambahkan ke favorit.")
    return redirect("menu_detail", pk=pk)


@login_required
def add_review(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                menu_item=item,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"]
            )
            messages.success(request, "Review ditambahkan.")
    return redirect("menu_detail", pk=pk)
