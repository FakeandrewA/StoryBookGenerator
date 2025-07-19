from pydantic import BaseModel , Field


##models
class GradeUserPrompt(BaseModel):
    """You are an intelligent AI, Our company is a story generator so we take in the user's prompt and generate a story ,therefore 
    you will see if a user's prompt is about generating a story or is it irrelevant about story generation, if yes the user's prompt is about story generation return yes else return no"""

    isStory:str = Field(description="Is user's prompt about story generation, yes or no")

class Story(BaseModel):
    """You are an creative AI, Our company is a story generator so we take in the user's prompt and generate a story, therefore for a user's provided story description,
    elaborate upon the prompt and create a story with 350-500 words maximum also generate the story's characters with detailed description from head to toe , then generate the story
    also make sure to give the story a title.
    """

    title:str = Field(description="A Great and catchy Title for the story")
    characterDescription:str = Field(description="A detailed description of characters from the story you are about to create.")
    story:str = Field(description="A story of 350-500 words with the characters you created.")

class Scenes(BaseModel):
    """You are an AI director, You take a story and create a narrative, You excel at splitting a given story into 5 different Scene and respective VoiceOver narrative for the 5 scences
    Make Sure:
        - The Scenes that you create are well written because that text will be given to a image generating model to generate the scene as image. also make sure you dont over prompt as well because the model will find it hard to follow
        - also generate the voiceovers that is relevant to the scene
        - there are cost constrains so you are to only generate 5 scenes and 5 respective voiceovers
    """
    scene1:str = Field(description="Scene 1 of the story with atmost detail for image generator")
    voiceover1:str = Field(description="Narrative for the Scene 1")

    scene2:str = Field(description="Scene 2 of the story with atmost detail for image generator")
    voiceover2:str = Field(description="Narrative for the Scene 2")

    scene3:str = Field(description="Scene 3 of the story with atmost detail for image generator")
    voiceover3:str = Field(description="Narrative for the Scene 3")

    scene4:str = Field(description="Scene 4 of the story with atmost detail for image generator")
    voiceover4:str = Field(description="Narrative for the Scene 4")

    scene5:str = Field(description="Scene 5 of the story with atmost detail for image generator")
    voiceover5:str = Field(description="Narrative for the Scene 5")