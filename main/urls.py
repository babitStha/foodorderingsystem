from django.urls import path
from . views import home, menu, cart, updateItem, orders, checkout,process_order,cancel

urlpatterns = [
    path("", home, name="home"),
    path("menu/", menu, name="menu"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("updateItem/", updateItem, name="updateItem"),
    path("process_order/", process_order, name="process_order"),
    path("orders/", orders, name="orders"),
    path("cancel/", cancel, name="cancel"),

]

