import os
import time
from langchain_core.exceptions import OutputParserException
from typing import TypedDict, NotRequired
from langgraph.graph import END,StateGraph
from .schemas import Story,Scenes
from .chains import scenesCreationChain,storyCreationChain,usersPromptGradingChain
from .imageGenerator import generateImage , titleImageGenerationTemplate , sceneImageGenerationTemplate

from django.conf import settings

static_dir = os.path.join(settings.BASE_DIR, 'storybookgenerator', 'static', 'storybookgenerator')

## State of the Graph
class BookState(TypedDict):
    userPrompt : str
    story: NotRequired[Story]
    scenes: NotRequired[Scenes]
    grade: NotRequired[str]
    userId : NotRequired[int]


## Nodes
def usersPrompt(state:BookState) -> BookState:
    print("Accessing User's prompt...")

    ## Checking proper tool call 
    MAX_TRIES = 3
    TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
    for attempt in range(MAX_TRIES):
        try:
            grade = usersPromptGradingChain.invoke({"userPrompt":state["userPrompt"]})
            break
        except Exception as e:
            error_message = str(e)
            if TARGET_ERROR in error_message:
                print(f"[Attempt {attempt+1}] Error: {e}")
                if attempt < MAX_TRIES - 1:
                    time.sleep(2) 
                    print("Sorry hit a Wall, Trying again...")
                else:
                    print("Max attempts reached. Try Again after some time")
                    raise OutputParserException("Parsing failed: Unexpected format.")
            else:
                raise Exception(e)
    ##

    state["grade"] = grade.isStory.strip().lower()
    return state

def gradeThePrompt(state):
    print("Analysing the User's Prompt...")
    if (state["grade"]=="no"):
        print("Ending the Graph... , User's request is Not Valid")
        return END
    else:
        return "storyCreator"
    
def storyCreator(state:BookState) -> BookState:
    print("Entering Story Creation Node...")

    ## Checking proper tool call
    MAX_TRIES = 3
    TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
    for attempt in range(MAX_TRIES):
        try:
            story = storyCreationChain.invoke({"userPrompt":state["userPrompt"]})
            break
        except Exception as e:
            error_message = str(e)
            if TARGET_ERROR in error_message:
                print(f"[Attempt {attempt+1}] Error: {e}")
                if attempt < MAX_TRIES - 1:
                    time.sleep(2) 
                    print("Sorry hit a Wall, Trying again...")
                else:
                    print("Max attempts reached. Try Again after some time")
                    raise OutputParserException("Parsing failed: Unexpected format.")
            else:
                raise Exception(e)
    ##
    print("Story Created+++")
    
    #### DEBUG
    # print("*"*20)
    # print("TITLE:",story.title)
    # print("CHARACTERS:",story.characterDescription)
    # print("STORY:",story.story)
    # print("STYLE:",story.style)
    # print("ONELINE:",story.oneline)
    # print("NUM_OF_SCENES:",story.numOfScenes)
    # print("*"*20)
    #### DEBUG

    state["story"] = story
    # state["userId"] = 1 ## edit this for request.user.id
    return state

def scenesCreator(state:BookState) -> BookState:
    print("Entering Scenes Creation Node...")
    story = state["story"]

    ## Checking proper tool call
    MAX_TRIES=3
    TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
    for attempt in range(MAX_TRIES):
        try:
            scenes = scenesCreationChain.invoke({"story":story.story,"characterDescription":story.characterDescription,"title":story.title,"n":story.numOfScenes})
            break
        except Exception as e:
            error_message = str(e)
            if TARGET_ERROR in error_message:
                print(f"[Attempt {attempt+1}] Error: {e}")
                if attempt < MAX_TRIES - 1:
                    time.sleep(2) 
                    print("Sorry hit a Wall, Trying again...")
                else:
                    print("Max attempts reached. Try Again after some time")
                    raise OutputParserException("Parsing failed: Unexpected format.")
            else:
                raise Exception(e)
    ##
    print("Created Scenes+++")

    #### DEBUG
    # print("*"*20)
    # print("SCENES:")
    # for i,scene in enumerate(scenes.scenes):
    #     print(i,scene)
    # print("VOICEOVERS:")
    # for i,scene in enumerate(scenes.voiceovers):
    #     print(i,scene)
    # print("*"*20)
    #### DEBUG

    state["scenes"] = scenes
    return state

def titleImageCreator(state:BookState) -> BookState:
    print("Entering Title Image Creation Node...")
    story = state["story"]
    prompt = titleImageGenerationTemplate.format(**{"oneline":story.oneline,"characterDescription":story.characterDescription,"story":story.story,"title":story.title})
    print(prompt)
    generateImage(prompt=prompt,filepath=f"{static_dir}/{state["userId"]}",filename="title.png")
    print("Created a Title Image+++")
    return state

def scenesImageCreator(state:BookState) -> BookState:
    print("Entering Scenes Image Creation Node...")
    story = state["story"]

    for i in range(story.numOfScenes):
        print(f"Creating Scene{i+1} Image...")
        previousScenes = "\n".join(state["scenes"].scenes[:i])
        currentScene = state["scenes"].scenes[i]
        kwargs = {"previousScenes":previousScenes,"style":story.style,"characterDescription":story.characterDescription,"story":story.story,"title":story.title,"currentScene":currentScene}
        prompt = sceneImageGenerationTemplate.format(**kwargs)
        print(prompt)
        generateImage(prompt=prompt,filepath=f"{static_dir}/{state["userId"]}",filename=f"scene{i+1}.png")
        print(f"created Scene{i+1} image+++")

    return state

graph = StateGraph(BookState)

graph.add_node("userPrompt",usersPrompt)
graph.add_node("storyCreator",storyCreator)
graph.add_node("scenesCreator",scenesCreator)
graph.add_node("titleImageCreator",titleImageCreator)
graph.add_node("scenesImageCreator",scenesImageCreator)

graph.set_entry_point("userPrompt")
graph.add_conditional_edges("userPrompt",gradeThePrompt,[END,"storyCreator"])
graph.add_edge("storyCreator","scenesCreator")
graph.add_edge("scenesCreator","titleImageCreator")
graph.add_edge("titleImageCreator","scenesImageCreator")
graph.add_edge("scenesImageCreator",END)

bookGenerator = graph.compile()