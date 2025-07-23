from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request,"storybookgenerator/homepage.html")

def book_view(request):
    return render(request, "storybookgenerator/book_view.html")

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time  # For simulating delay

def homepage(request):
    return render(request, "storybookgenerator/homepage.html")

def book_view(request):
    return render(request, "storybookgenerator/book_view.html")

@csrf_exempt
def generate_story(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            # Simulated delay to mimic slow API
            time.sleep(3)

            # 🔁 You can replace this block with actual AI story generator logic
            story_text = f"Once upon a time... your story begins with: {prompt}"
            image_urls = [
                "https://example.com/image1.png",
                "https://example.com/image2.png"
            ]

            return JsonResponse({
                "success": True,
                "story": story_text,
                "images": image_urls
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)