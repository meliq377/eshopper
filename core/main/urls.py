from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('category/<str:slug>', CategoryListView.as_view(), name='category'),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path("cart", cart, name="cart"),
    path("checkout", checkout, name="checkout"),
    path("updatecart", updateCart, name="updatecart"),
    path("updatequantity", updateQuantity, name="updatequantity"),

]
