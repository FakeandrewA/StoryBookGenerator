from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .schemas import Scenes,Story,GradeUserPrompt
from .promptTemplates import usersPromptGradingTemplate,storyCreationTemplate,scenesCreationTemplate,titleImageGenerationTemplate

## Uses's Prompt Grading Chain
usersPromptGrader = ChatGroq(model="llama3-70b-8192").with_structured_output(GradeUserPrompt)
usersPromptGradingChain = usersPromptGradingTemplate | usersPromptGrader

## Story Creation Chain 
storyCreator = ChatGroq(model="llama3-70b-8192").with_structured_output(Story)
storyCreationChain = storyCreationTemplate | storyCreator

## Scenes Creation Chain
scenesCreator = ChatGroq(model="llama3-70b-8192").with_structured_output(Scenes)
scenesCreationChain = scenesCreationTemplate | scenesCreator

