from django.urls import path
from .views import homepage, book_view, register

app_name = "storybookgenerator"

urlpatterns = [
    path("homepage/", homepage, name="homepage"),
    path("book/", book_view, name="book_view"),
    path("register/", register, name="register"),
]
