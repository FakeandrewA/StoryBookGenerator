from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

##ChatPromptTemplates
usersPromptGradingTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are amazing at detecting flaws, see the user's prompt and
    detect if the prompt has anything relevent about story generation if yes return yes else return no
    
    always call the tool "GradeUserPrompt" to parse your results into attributes

     """),
    ("human","user's prompt:\n{users_prompt}")
])

storyCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are very Creative at creating a story even from a one line, take in user's prompt create a story based on what user mentioned
     make sure the story has good struture without logical flaws, and has an interesting ending.
     
     - first create the characters of the story with atmost details,
        The Faces of the Characters are the most important thing, so explain their facial structure to the point were it seems like a obsession
        Then other parts of theSir body , explain these like a tailor who takes measurement it need to be obsessively perfect, dont mention any wearables like clothes because they can be changed
        always use this convention:
                   Charater 1: ...
                   Charater 2: ...
                   ....
                   Character n: ... 
     
     - Use Both User's Prompt and The Chracters You Created to Create a Story of 1000 words minimum
     
     - after the story creation , give it a title which is apt for the story

     - always choose a style for the story that is apt for the story, 
       For example : Cartoon, Anime art , Realistic and etc. to help our image generators to be consistent with styles while generating images from your story
     
     - also to help our image generators to create a title with a cover image , write a one line of the whole story
     
     - also to help our picture book scene creator , give us a estimate of num of scenes required to create your story into a picture book

    always call the tool "Story" to parse your story and other details into attributes
      
     """),
     ("human","user's prompt:\n{users_prompt}")
])

scenesCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are an excellent AI director, Who splits a given story into {n} well written scenes and 
     respective {n} voiceovers for the scenes, Make sure to create the scenes with well format and structure 
     because it will be given to a image generating model to generate the image for the scene so describe the scene almost like you are describing the scene pixel by pixel , use upto 200 word to describe
    
     
     Always Create Scenes and Voiceovers with prefix:
     scene n : ....
     voiceover n : ...

     Make sure the all scenes together convey what the original story has to offer 
     create the scenes in such a way that each is telling the stories next sequence in a logical order 
     sometimes in chronological order
    
     Always use the tool "Scenes" to parse your scenes and voiceovers into attributes

     """),
     ("human","\n\nTitle:\n{title}\nCharacters:\n{character_description}\nStory:\n{story}")
])
