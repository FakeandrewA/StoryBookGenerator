from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

##ChatPromptTemplates
usersPromptGradingTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are amazing at detecting flaws, see the user's prompt and
    detect if the prompt has anything relevent about story generation if yes return yes else return no
    
    always call the tool "GradeUserPrompt" to parse your results into attributes

     """),
    ("human","user's prompt:\n{userPrompt}")
])

storyCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are very Creative at creating a story even from a one line, take in user's prompt create a story based on what user mentioned
     make sure the story has good struture without logical flaws, and has an interesting ending.
     You have to always generate a kids story with a moral ending
     
     - give the story a title      
     
     - first create the characters of the story with atmost details,
        Take the characters from popular sitcoms , TV shows, anime or kids shows so that the characters are consistent in each generation of image 
        for example if you want a kid character , name it the young sheldon , etc. Dont Give Them Nicknames use  their full names
        because the image generators can be able know how would the character look like 
        give them a age as well
        always use this convention:
                   Charater 1: ...
                   Charater 2: ...
                   ....
                   Character n: ... 
     
     - Use Both User's Prompt and The Chracters You Created to Create a Story of 500 words minimum
     
     - always choose a style for the story that is apt for the story, 
       For example : Cartoon, Anime art , Realistic and etc. to help our image generators to be consistent with styles while generating images from your story
    
     - To Help the Image generator generate the title , Describe the Title image with details , describe all things like what is the title, where will the title be place , what characters are in the title with their description, their placement and position of their body in the image and everything 
    
     always call the tool "Story" to parse your story and other details into attributes
      
     """),
     ("human","user's prompt:\n{userPrompt}")
])

scenesCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""
     You are an excellent AI director, Who splits a given story into {n} well written scenes and 
     respective {n} voiceovers for the scenes,All the Scenes Should be meaningful.

     You will describe the scene at a great detail like this,
     for example: if a scene has a man standing near a poll , start describing the background , position of the man , etc,.
     prompt : ``` A black man in his 30s standing near a white poll in the rigth half of screen looking at the road the photo is taken in the new york street where 
                  cars moving in the backgroung and people walking past the poll where the man is standing ```
     see how I described everything in the picture , so you also generate as if you are describe the scene like seeing the scene in 
     
     
     Whenever a previous Scene need to be in the next scene to make sense then include that scene also in the scene
     
     for example;
     - A was sitting with B
     - When A was sitting with B , then C arrived the scene

     instead of doing this 
     - A was sitting with B
     - C arrived the scene  (this causes image generator lose context)


     Always use the tool "Scenes" to parse your scenes and voiceovers into attributes

     """),
     ("human","\n\nTitle:\n{title}\nCharacters:\n{characterDescription}\nStory:\n{story}")
])
