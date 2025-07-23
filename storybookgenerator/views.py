from django.shortcuts import redirect
from .models import Scene

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
    story = request.session.get("story", "")
    images = request.session.get("images", [])
    scenes = Scene.objects.all()
    return render(request, "storybookgenerator/book_view.html", {
        "story": story,
        "images": images,
        "scenes": scenes
    })

@csrf_exempt
def generate_story(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            time.sleep(3)

            story_text = f"Once upon a time... your story begins with: {prompt}"
            image_urls = [
                "https://example.com/image1.png",
                "https://example.com/image2.png"
            ]

            # Save to session for dashboard/book_view
            request.session['story'] = story_text
            request.session['images'] = image_urls

            return JsonResponse({
                "success": True,
                "story": story_text,
                "images": image_urls
            })
        

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)   


def update_scene(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(id=scene_id)
        scene.text = request.POST.get("text", "")
        scene.save()
    return redirect("storybookgenerator:book_view")

def delete_scene(request, scene_id):
    Scene.objects.filter(id=scene_id).delete()
    return redirect("storybookgenerator:book_view")