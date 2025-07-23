from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages, redirect
from .storybookagent.graph import loadBookGenerator
from django.conf import settings
import os
from django.contrib.auth.models import User

static_dir = os.path.join(settings.BASE_DIR, "storybookgenerator", "static", "storybookgenerator")
bookGenerator = loadBookGenerator(static_dir, debug=True, timeout_seconds=20, max_tries_for_connection_retry=2, max_tries_for_graph_retry=2)
# ────────────────────────────── SETUP INSTRUCTIONS ──────────────────────────────
# 1. Visit https://api.together.xyz and generate an API key.
#    - Copy and paste this key into `.env.example` under TOGETHER_API_KEY.
#
# 2. Visit https://groq.com and create a GROQ API key.
#    - Paste this key into `.env.example` under GROQ_API_KEY.
#
# 3. Rename `.env.example` to `.env` so that environment variables can be loaded.
#
# 4. Set up the virtual environment (if not already done):
#    - On Windows:
#        python -m venv venv
#        .\venv\Scripts\activate
#    - On macOS/Linux:
#        python3 -m venv venv
#        source venv/bin/activate
#
# 5. Install all required packages:
#    pip install -r requirements.txt
#
# After this setup, your development environment should be ready to run the book generator.


# ────────────────────────────── USAGE INSTRUCTIONS ──────────────────────────────
# To generate a storybook, use the following:

# book = bookGenerator.invoke({
#     "userPrompt": "<your prompt here>",
#     "userId": request.user.id
# })

# The `book` output is a dictionary with the following structure:

# book["userPrompt"] → str                   # The original prompt from the user
# book["story"]      → Story object          # Structured story data
#     ├─ title               → str           # Title of the story
#     ├─ titleImagePrompt    → str           # Detailed image prompt for the title illustration
#     ├─ characterDescription→ str           # Character descriptions for scene generation
#     ├─ story               → str           # The full story text (~500 words)
#     ├─ style               → str           # Visual/artistic style for images
#     └─ numOfScenes         → int           # Number of visual scenes in the story (default: 10)

# book["scenes"]     → Scenes object         # Scene descriptions and voiceovers
#     ├─ scenes      → list[str]             # List of detailed scene prompts (in order)
#     └─ voiceovers  → list[str]             # Matching narration lines for each scene

# For full schema definitions, refer to: `storybookagent/schemas.py`
# ────────────────────────────── VIEWS ────────────────────────────
# Create your views here.


def homepage(request):
    return render(request,"storybookgenerator/homepage.html")

def book_view(request):
    book = bookGenerator.invoke({"userPrompt":"Create a Story about a Crocodile in florida","userId":1})
    return render(request, "storybookgenerator/book_view.html")

def register_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("storybookgenerator:homepage")
        return render(request, "storybookgenerator/register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        new_user = User.objects.create_user(
            username=username,
            email=email,
        )
        new_user.set_password(password)
        new_user.save()
        return redirect("storybookgenerator:login")
        


def login_view(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('storybookgenerator:homepage')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

