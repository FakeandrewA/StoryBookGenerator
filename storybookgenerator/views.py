from django.shortcuts import render
from .storybookagent.graph import bookGenerator

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
