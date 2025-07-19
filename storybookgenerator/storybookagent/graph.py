import uuid

from typing import TypedDict,List , NotRequired
from langgraph.graph import END,StateGraph
from langchain_core.prompts import PromptTemplate
from storygenerator.schemas import Story,Scenes
from storygenerator.chains import scenesCreationChain,storyCreationChain,usersPromptGradingChain
from storygenerator.imagegenerator import generateImage

## State of the Graph
class BookState(TypedDict):
    users_prompt : str
    story: NotRequired[Story]
    scenes: NotRequired[Scenes]
    grade: NotRequired[str]
    users_id : NotRequired[int]

##templates
titleImageGenerationTemplate = PromptTemplate.from_template("""
{character_description}\n\n{story}\n\
    Create a Title page of the Book for this story book,
    - Anywhere in the image place this title : '{title}' **ALWAYS INCLUDE THIS TITLE IN THE IMAGE** 
    -Make Sure Texts you create in the image is accurate and not a gibberish so focus more on that
    -Dont Explicitly name things like 'Title of the book' near the title 
""") 

sceneImageGenerationTemplate = PromptTemplate.from_template("""
You are a creative AI director who is best at setting the scene from imagination to image.
For the given story and Characters, create the scene mentioned , you will have a context of what happened before and what is the current scene
This is the Story:
{title}
{story}
This is the Character description:
{character_description}
these are the the previous scenes:
{previous_scenes}
the current scene:
(The Above details are only for your context of what is theme and who are the characters involved in the story, so when generating your image only focus on the current scene while taking the aspects of the details provided above)
{current_scene}  
""")

## Nodes
def usersPrompt(state:BookState) -> BookState:
    print("Accessing User's prompt...")
    grade = usersPromptGradingChain.invoke({"users_prompt":state["users_prompt"]})
    state["grade"] = grade.isStory.strip().lower()
    return state

def gradeThePrompt(state):
    print("Analysing the User's Prompt...")
    if (state["grade"]=="no"):
        print("Ending the Graph... , User's request is Not Valid")
        return END
    else:
        return "storycreator"
    
def storyCreator(state:BookState) -> BookState:
    print("Entering Story Creation Node...")
    story = storyCreationChain.invoke({"users_prompt":state["users_prompt"]})
    print("Story Created...")
    state["story"] = story
    state["users_id"] = uuid.uuid4()
    return state

def titleImageCreator(state:BookState) -> BookState:
    print("Entering Title Image Creation Node...")
    story = state["story"]
    prompt = titleImageGenerationTemplate.format(**{"character_description":story.characterDescription,"story":story.story,"title":story.title})
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="title.png")
    print("Created a Title Image....")
    return {}

def scenesCreator(state:BookState) -> BookState:
    print("Entering Scenes Creation Node... ")
    story = state["story"]
    scenes = scenesCreationChain.invoke({"story":story.story,"character_description":story.characterDescription,"title":story.title})
    print("Created Scenes")
    state["scenes"] = scenes
    print(scenes)
    return state

def scene1ImageCreator(state:BookState) -> BookState:
    print("Entering Scene 1 Image Creation Node...")
    story = state["story"]
    previous_scenes = "NO PREVIOUS SCENES"
    current_scene = state["scenes"].scenes[0]
    kwargs = {"character_description":story.characterDescription,"story":story.story,"title":story.title, "previous_scenes":previous_scenes,"current_scene":current_scene}
    prompt = sceneImageGenerationTemplate.format(**kwargs)
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="scene1.png")
    print("created scene 1 image")
    return {}

def scene2ImageCreator(state:BookState) -> BookState:
    print("Entering Scene 2 Image Creation Node...")
    story = state["story"]
    previous_scenes = "\n\n".join([f"scene_{i}\n"+scene for i,scene in enumerate(state["scenes"].scenes) if i < 1])
    current_scene = state["scenes"].scenes[1]
    kwargs = {"character_description":story.characterDescription,"story":story.story,"title":story.title, "previous_scenes":previous_scenes,"current_scene":current_scene}
    prompt = sceneImageGenerationTemplate.format(**kwargs)
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="scene2.png")
    print("created scene 2 image")
    return {}

def scene3ImageCreator(state:BookState) -> BookState:
    print("Entering Scene 3 Image Creation Node...")
    story = state["story"]
    previous_scenes = "\n\n".join([f"scene_{i}\n"+scene for i,scene in enumerate(state["scenes"].scenes) if i < 2])
    current_scene = state["scenes"].scenes[2]
    kwargs = {"character_description":story.characterDescription,"story":story.story,"title":story.title, "previous_scenes":previous_scenes,"current_scene":current_scene}
    prompt = sceneImageGenerationTemplate.format(**kwargs)
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="scene3.png")
    print("created scene 3 image")
    return {}

def scene4ImageCreator(state:BookState) -> BookState:
    print("Entering Scene 4 Image Creation Node...")
    story = state["story"]
    previous_scenes = "\n\n".join([f"scene_{i}\n"+scene for i,scene in enumerate(state["scenes"].scenes) if i < 3])
    current_scene = state["scenes"].scenes[3]
    kwargs = {"character_description":story.characterDescription,"story":story.story,"title":story.title, "previous_scenes":previous_scenes,"current_scene":current_scene}
    prompt = sceneImageGenerationTemplate.format(**kwargs)
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="scene4.png")
    print("created scene 4 image")
    return {}

def scene5ImageCreator(state:BookState) -> BookState:
    print("Entering Scene 5 Image Creation Node...")
    story = state["story"]
    previous_scenes = "\n\n".join([f"scene_{i}\n"+scene for i,scene in enumerate(state["scenes"].scenes) if i < 4])
    current_scene = state["scenes"].scenes[4]
    kwargs = {"character_description":story.characterDescription,"story":story.story,"title":story.title, "previous_scenes":previous_scenes,"current_scene":current_scene}
    prompt = sceneImageGenerationTemplate.format(**kwargs)
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="scene5.png")
    print("created scene 5 image")
    return {}

graph = StateGraph(BookState)

graph.add_node("usersprompt",usersPrompt)
graph.add_node("storycreator",storyCreator)
graph.add_node("titleimagecreator",titleImageCreator)
graph.add_node("scenescreator",scenesCreator)
graph.add_node("scene1imagecreator",scene1ImageCreator)
graph.add_node("scene2imagecreator",scene2ImageCreator)
graph.add_node("scene3imagecreator",scene3ImageCreator)
graph.add_node("scene4imagecreator",scene4ImageCreator)
graph.add_node("scene5imagecreator",scene5ImageCreator)


graph.set_entry_point("usersprompt")
graph.add_conditional_edges("usersprompt",gradeThePrompt,[END,"storycreator"])
graph.add_edge("storycreator","titleimagecreator")
graph.add_edge("titleimagecreator",END)
graph.add_edge("storycreator","scenescreator")
graph.add_edge("scenescreator","scene1imagecreator")
graph.add_edge("scenescreator","scene2imagecreator")
graph.add_edge("scenescreator","scene3imagecreator")
graph.add_edge("scenescreator","scene4imagecreator")
graph.add_edge("scenescreator","scene5imagecreator")
graph.add_edge("scene1imagecreator",END)
graph.add_edge("scene2imagecreator",END)
graph.add_edge("scene3imagecreator",END)
graph.add_edge("scene4imagecreator",END)
graph.add_edge("scene5imagecreator",END)

app = graph.compile()

