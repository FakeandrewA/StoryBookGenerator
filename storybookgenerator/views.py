from django.shortcuts import render, redirect
from .storybookagent.graph import bookGenerator
from django.contrib.auth.models import User

## DO THIS
# go to api.together.xyz and create a api key and copy paste it in the .env.example
# then go to groq.com and create a api key and copy paste it in the .env.example
# rename the .env.example -> .env
# then activate the venv
# source venv/Scripts/activate
# then
# pip install -r requirements.txt
#
#now everything should work

## How To Use This bookGenerator
##
## book = bookGenerator.invoke({"userPrompt":"<prompt>","userId":request.user.id})
##
## returns:
## a dictionary with these attributes
## book["userPrompt"] -> str
## book["story"] -> Story object
##                          \___>> book["story"].title -> str
##                           \___>> book["story"].characterDescription -> str
##                            \___>> book["story"].story -> str
##                             \___>> book["story"].oneline -> str
##                              \___>> book["story"].style -> str
##                               \___>> book["story"].numOfScenes -> int
## book["scenes"] -> Scenes object
##                            \___>> book["scenes"].scenes -> list[str]
##                             \___>> book["scenes"].voiceovers -> list[str]
##
## for more details go to storybookagent/schemas.py to read more , also checkout storybookagent

# Create your views here.
def homepage(request):
    return render(request,"storybookgenerator/homepage.html")

def book_view(request):
    return render(request, "storybookgenerator/book_view.html")

def register(request):
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
        

