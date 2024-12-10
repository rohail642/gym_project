from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="register"),
    path("login/", views.login_view, name="signin"),
    path("payment/callback", views.payment_callback, name="payment_callback"),
]