from django.urls import path
from . import views

app_name = "storybookgenerator"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("book/", views.book_view, name="book"),
    path("login/",views.login_view,name="login"),
     path('register/',views.register_view, name='register'),
   
]
