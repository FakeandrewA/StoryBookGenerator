import os
import time
from pydantic import BaseModel
from typing import List
from langchain_core.exceptions import OutputParserException
from typing import TypedDict, NotRequired
from langgraph.graph import END,StateGraph
from .schemas import Story,Scenes
from .chains import scenesCreationChain,storyCreationChain,usersPromptGradingChain
from .imageGenerator import generateImage , titleImageGenerationTemplate , sceneImageGenerationTemplate

from django.conf import settings

class IsTitleImageGenerated(BaseModel):
    isTitleImageGenerated:bool = False
    noOftries:int = 0

## State of the Graph
class BookState(TypedDict):
    userPrompt : str
    story: NotRequired[Story]
    scenes: NotRequired[Scenes]
    grade: NotRequired[str]
    userId : int
    isTitleImageGenerated: NotRequired[IsTitleImageGenerated]
    garbage:NotRequired[List[int]]



def loadBookGenerator(dir:str,debug=False,timeout_seconds:int=25,max_tries_for_connection_retry:int=3,max_tries_for_graph_retry:int=2):
    """
    Initializes and compiles a LangGraph pipeline (StateGraph) for generating an illustrated storybook 
    based on a user's prompt. This includes prompt validation, story creation, scene generation, 
    and image generation for both the title and scenes.

    Args:
        dir (str): 
            Directory path where generated images will be saved. Each user's images are stored in 
            a subdirectory named by their user ID.
        
        debug (bool, optional): 
            If True, prints intermediate debugging information such as prompts, story details, and scene outputs. 
            Default is False.
        
        timeout_seconds (int, optional): 
            Timeout for each image generation operation. Default is 25 seconds.

        max_tries_for_connection_retry (int, optional): 
            Maximum number of retries for function/tool call failures like LLM API calls. 
            Used in prompt grading, story creation, and scene generation. Default is 3.

        max_tries_for_graph_retry (int, optional): 
            Maximum number of retries within the LangGraph for critical nodes like image generation. 
            Default is 2.

    Returns:
        bookGenerator (Runnable): 
            A compiled LangGraph object that can be run with a valid `BookState` input to generate 
            a complete storybook pipeline including:
                - Prompt validation
                - Story generation
                - Scene script generation
                - Title image creation with retry logic
                - Scene image generation with retry + garbage collection for failed scenes

    Raises:
        OutputParserException: 
            Raised if the language model fails to return valid output even after retries.

        Exception: 
            For other unexpected errors such as API connection errors or formatting issues.
    """
    ## Nodes
    def usersPrompt(state:BookState) -> BookState:
        print("Accessing User's prompt...")

        ## Checking proper tool call 
        TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
        for attempt in range(max_tries_for_connection_retry):
            try:
                grade = usersPromptGradingChain.invoke({"userPrompt":state["userPrompt"]})
                break
            except Exception as e:
                error_message = str(e)
                if TARGET_ERROR in error_message:
                    print(f"[Attempt {attempt+1}] Error: {e}")
                    if attempt < max_tries_for_connection_retry - 1:
                        time.sleep(2) 
                        print("Sorry hit a Wall, Trying again...")
                    else:
                        print("Max attempts reached. Try Again after some time")
                        raise OutputParserException("Parsing failed: Unexpected format.")
                else:
                    raise Exception(e)
        state["garbage"] = []
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
        TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
        for attempt in range(max_tries_for_connection_retry):
            try:
                story = storyCreationChain.invoke({"userPrompt":state["userPrompt"]})
                break
            except Exception as e:
                error_message = str(e)
                if TARGET_ERROR in error_message:
                    print(f"[Attempt {attempt+1}] Error: {e}")
                    if attempt < max_tries_for_connection_retry - 1:
                        time.sleep(2) 
                        print("Sorry hit a Wall, Trying again...")
                    else:
                        print("Max attempts reached. Try Again after some time")
                        raise OutputParserException("Parsing failed: Unexpected format.")
                else:
                    raise Exception(e)
        ##
        print("Story Created+++")
        
        if debug:
            print("*"*20)
            print("TITLEIMAGEPROPMT",story.titleImagePrompt)
            print("TITLE:",story.title)
            print("CHARACTERS:",story.characterDescription)
            print("STORY:",story.story)
            print("STYLE:",story.style)
            print("NUM_OF_SCENES:",story.numOfScenes)
            print("*"*20)

        state["story"] = story
        return state

    def scenesCreator(state:BookState) -> BookState:
        print("Entering Scenes Creation Node...")
        story = state["story"]

        ## Checking proper tool call
        TARGET_ERROR = "Failed to call a function. Please adjust your prompt."
        for attempt in range(max_tries_for_connection_retry):
            try:
                scenes = scenesCreationChain.invoke({"story":story.story,"characterDescription":story.characterDescription,"title":story.title,"n":story.numOfScenes})
                break
            except Exception as e:
                error_message = str(e)
                if TARGET_ERROR in error_message:
                    print(f"[Attempt {attempt+1}] Error: {e}")
                    if attempt < max_tries_for_connection_retry - 1:
                        time.sleep(2) 
                        print("Sorry hit a Wall, Trying again...")
                    else:
                        print("Max attempts reached. Try Again after some time")
                        raise OutputParserException("Parsing failed: Unexpected format.")
                else:
                    raise Exception(e)
        ##
        print("Created Scenes+++")

        if debug:
            print("*"*20)
            print("SCENES:")
            for i,scene in enumerate(scenes.scenes):
                print(i,scene)
            print("VOICEOVERS:")
            for i,scene in enumerate(scenes.voiceovers):
                print(i,scene)
            print("*"*20)

        state["scenes"] = scenes
        return state

    def titleImageCreator(state:BookState) -> BookState:
        print("Entering Title Image Creation Node...")
        story = state["story"]
        prompt = titleImageGenerationTemplate.format(**{"titleImagePrompt":story.titleImagePrompt})
        print(prompt)
        generateImage(timeout_seconds=timeout_seconds,prompt=prompt,filepath=f"{dir}/{state['userId']}",filename="title.png")
        
        # Initialize if not exists
        if "isTitleImageGenerated" not in state:
            state["isTitleImageGenerated"] = IsTitleImageGenerated()
            
        if "title.png" in os.listdir(f"{dir}/{state['userId']}"):
            state["isTitleImageGenerated"].isTitleImageGenerated = True


        return state
    
    def titleImageRouter(state:BookState):
         if state["isTitleImageGenerated"].isTitleImageGenerated:
             print("Created a Title Image+++")
             return "scenesImageCreator"
         else:
             if state["isTitleImageGenerated"].noOftries < max_tries_for_graph_retry: 
                state["isTitleImageGenerated"].noOftries+=1
                return "titleImageCreator"
             else:
                return END
    
    def scenesImageCreator(state:BookState) -> BookState:
        print("Entering Scenes Image Creation Node...")
        story = state["story"]

        for i in range(story.numOfScenes):
            print(f"Creating Scene{i+1} Image...")
            currentScene = state["scenes"].scenes[i]
            kwargs = {"style":story.style,"currentScene":currentScene}
            prompt = sceneImageGenerationTemplate.format(**kwargs)
            print(prompt)
            generateImage(timeout_seconds=timeout_seconds,prompt=prompt,filepath=f"{dir}/{state['userId']}",filename=f"scene{i+1}.png")
            if f"scene{i+1}.png" not in os.listdir(f"{dir}/{state['userId']}"):
                state["garbage"].append(i)
                print(f"Couldn't create Scene{i+1} image !!!")
            else:
                print(f"created Scene{i+1} image+++")

        return state

    def scenesImageGarbageCollector(state:BookState):
        tries = 0
        story = state["story"]
        print("Entering Scenes Image Garbage Collector Node...")
        if not state["garbage"]:
            print("No Garbage Found, Returning...")
            return state
        print("Garbage Found, Collecting...")
        print(f"Garbage: {state['garbage']}")
        print(f"Number of Garbage: {len(state['garbage'])}")
        while state["garbage"] and tries!=max_tries_for_graph_retry:
            i = state["garbage"][-1]
            print(f"Creating Scene{i+1} Image again......")
            currentScene = state["scenes"].scenes[i]
            kwargs = {"style":story.style,"currentScene":currentScene}
            prompt = sceneImageGenerationTemplate.format(**kwargs)
            print(prompt)
            generateImage(timeout_seconds=timeout_seconds,prompt=prompt,filepath=f"{dir}/{state["userId"]}",filename=f"scene{i+1}.png",max_retries=1)
            if f"scene{i+1}.png" not in os.listdir(f"{dir}/{state['userId']}"):
                tries+=1
                print(f"Couldn't create Scene{i+1} image !!!,Trying Again")
            else:
                state["garbage"].pop()
                print(f"created Scene{i+1} image+++")
        
        return state


    graph = StateGraph(BookState)

    graph.add_node("userPrompt",usersPrompt)
    graph.add_node("storyCreator",storyCreator)
    graph.add_node("scenesCreator",scenesCreator)
    graph.add_node("titleImageCreator",titleImageCreator)
    graph.add_node("scenesImageCreator",scenesImageCreator)
    graph.add_node("scenesImageGarbageCollector",scenesImageGarbageCollector)

    graph.set_entry_point("userPrompt")
    graph.add_conditional_edges("userPrompt",gradeThePrompt,[END,"storyCreator"])
    graph.add_edge("storyCreator","scenesCreator")
    graph.add_edge("scenesCreator","titleImageCreator")
    graph.add_conditional_edges("titleImageCreator",titleImageRouter,["scenesImageCreator","titleImageCreator",END])
    graph.add_edge("scenesImageCreator","scenesImageGarbageCollector")
    graph.add_edge("scenesImageGarbageCollector",END)

    bookGenerator = graph.compile()

    return bookGenerator