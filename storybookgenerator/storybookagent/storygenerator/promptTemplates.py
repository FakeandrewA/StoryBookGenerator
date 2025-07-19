from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

##ChatPromptTemplates
usersPromptGradingTemplate = ChatPromptTemplate.from_messages([
    ("system","You are amazing at detecting flaws, see the user's prompt and"
    "detect if the prompt has anything relevent about story generation if yes return yes else return no"),
    ("human","user's prompt:\n{users_prompt}")
])

storyCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""You are very Creative at creating a story even from a one line, take in user's prompt create a story based on what user mentioned,
     follow a structured approach ,
     first create the characters of the story with atmost details, 
     then use those Characters to create a story based on uses's prompt with 350-500 words, 
     Focus On these Points for the Story:
        - A well developed characters
        - A good Story line with some moral ending
            so from the start keep in mind that there is a moral ending so develop the story line based on that
        - Provide a Title for the Story's FrontPage
     """),
     ("human","user's prompt:\n{users_prompt}")
])

scenesCreationTemplate = ChatPromptTemplate.from_messages([
    ("system","""You are a excellent AI director, Who splits a given story into 5 well written scenes and 
     respective 5 voiceovers for the scenes,Make sure to create the scenes with well format and structure 
     because it will be given to a image generating model to generate the image for the scene also make 
     sure to not over prompt as it will make the model confused"""),
     ("human","Story:\n\nTitle:\n{title}\nCharacters:\n{character_description}\nStory:\n{story}")
])


#templates
titleImageGenerationTemplate = PromptTemplate.from_template("""
{character_description}\n\n{story}\n\
    Create a Title page of the Book for this story book,
    - Anywhere in the image place this title : '{title}'  
    -Make Sure Texts you create in the image is accurate and not a gibberish so focus more on that
    -Dont Explicitly name things like 'Title of the book' near the title 
""") 