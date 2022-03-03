from django.urls import path
from . views import home, menu, cart, updateItem, orders, checkout

urlpatterns = [
    path("", home, name="home"),
    path("menu/", menu, name="menu"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("updateItem/", updateItem, name="updateItem"),
    path("orders/", orders, name="orders"),

]

