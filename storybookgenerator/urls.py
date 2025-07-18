from django.urls import path
from .views import homepage

app_name = "storybookgenerator"

urlpatterns = [
    path("homepage/", homepage, name="homepage"),
]
