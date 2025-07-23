from django.urls import path
from .views import homepage, book_view, login_view, register_view, logout_view

app_name = "storybookgenerator"

urlpatterns = [
    path("homepage/", homepage, name="homepage"),
    path("book/", book_view, name="book_view"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
