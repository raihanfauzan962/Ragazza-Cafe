from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_list, name="menu_list"),
    path("menu/<int:pk>/", views.menu_detail, name="menu_detail"),
    path("menu/<int:pk>/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/", views.order_list, name="order_list"),
    path("order/<int:pk>/", views.order_detail, name="order_detail"),
    path("favorites/", views.favorites_list, name="favorites"),
    path("menu/<int:pk>/favorite/", views.add_to_favorites, name="add_to_favorites"),
    path("menu/<int:pk>/review/", views.add_review, name="add_review"),
    
]

