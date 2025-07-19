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
    - Anywhere in the image place this title : '{title}'  
    -Make Sure Texts you create in the image is accurate and not a gibberish so focus more on that
    -Dont Explicitly name things like 'Title of the book' near the title 
""") 

## Nodes
def usersPrompt(state:BookState) -> BookState:
    grade = usersPromptGradingChain.invoke({"users_prompt":state["users_prompt"]})
    return {
            "users_prompt":state["users_prompt"],
            "grade" : grade.isStory.strip().lower()
        }

def gradeThePrompt(state):
    if (state["grade"]=="no"):
        print("Ending the Graph... , User's request is Not Valid")
        return END
    else:
        print("Entering Story Creation Node...")
        return "storycreator"
    
def storyCreator(state:BookState) -> BookState:
    story = storyCreationChain.invoke({"users_prompt":state["users_prompt"]})
    print("Story Created ...")
    print("Entering Title Image Creation Node...")
    return {"users_prompt":state["users_prompt"],"grade" : state["grade"],"story":story,"users_id":uuid.uuid4()}

def titleImageCreator(state:BookState) -> BookState:
    story = state["story"]
    prompt = titleImageGenerationTemplate.format(**{"character_description":story.characterDescription,"story":story.story,"title":story.title})
    generateImage(prompt=prompt,filepath=f"stories/{state["users_id"]}",filename="title.png")
    print("Created a Title Image....")
    return state

graph = StateGraph(BookState)

graph.add_node("usersprompt",usersPrompt)
graph.add_node("storycreator",storyCreator)
graph.add_node("titleimagecreator",titleImageCreator)

graph.set_entry_point("usersprompt")
graph.add_conditional_edges("usersprompt",gradeThePrompt,[END,"storycreator"])
graph.add_edge("storycreator","titleimagecreator")
graph.add_edge("storycreator",END)

app = graph.compile()

