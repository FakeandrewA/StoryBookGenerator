from pydantic import BaseModel , Field
from typing import List

##models
class GradeUserPrompt(BaseModel):
    """A Grade Parser Tool used for parsing the result."""

    isStory:str = Field(description="Is user's prompt about story generation, yes or no")

class Story(BaseModel):
    """A Story Parser Tool used for parsing the story's title , the characters, the story, the style, the oneline and 
    the number of scenes to change the story into picturebook"""

    title:str = Field(description="title image description at a great Detail")
    characterDescription:str = Field(description="A detailed description of characters from the story you are about to create.")
    story:str = Field(description="A story of 500 words with the characters you created.")
    style:str = Field(description="The Whole Style of the story's setting")
    numOfScenes:int = 10
    

class Scenes(BaseModel):
    """A Scenes and Voiceovers Parser Tool used for parsing the scenes and voiceovers as list of strings."""

    scenes:List[str] = Field(description="Scenes of the story with atmost detail for the image generator, DO NOT MESS UP the order")
    voiceovers:List[str] = Field(description="Narratives of the scenes, DO NOT MESS UP the Order")