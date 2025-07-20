import re
from django.shortcuts import render
import os 
from django.conf import settings

def natural_sort_key(filename):
    # Extract numeric parts for natural sorting (e.g., scene2 before scene10)
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', filename)]


# Create your views here.
def homepage(request):
    return render(request,"storybookgenerator/homepage.html")

def book_view(request):
    print("BASE_DIR:", settings.BASE_DIR)

    user_id = "1"
    static_user_dir = os.path.join(settings.BASE_DIR, "storybookgenerator","static", "storybookgenerator", user_id)
    scenes = []

    # Get all image files
    all_files = [f for f in os.listdir(static_user_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    # Put 'title.png' first if present
    if 'title.png' in all_files:
        all_files.remove('title.png')
        ordered_files = ['title.png'] + sorted(all_files, key=natural_sort_key)
    else:
        ordered_files = sorted(all_files, key=natural_sort_key)

    # Build the scenes list
    for image in ordered_files:
        image_path = os.path.join("storybookgenerator", user_id, image).replace("\\", "/")
        scenes.append({
            "img": image_path,
            "text": f"Text for the {image}"
        })

    return render(request, "storybookgenerator/book_view.html",{"scenes":scenes})
