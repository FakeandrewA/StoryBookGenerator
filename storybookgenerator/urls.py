from django.urls import path
from .views import homepage, book_view, generate_story  # ✅ Make sure to import it

app_name = "storybookgenerator"

urlpatterns = [
    path("homepage/", homepage, name="homepage"),
    path("book/", book_view, name="book_view"),
    path("generate-story/", generate_story, name="generate_story"),  # ✅ Add this line
]
