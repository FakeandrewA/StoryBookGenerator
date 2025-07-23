from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .schemas import Scenes,Story,GradeUserPrompt
from .promptTemplates import usersPromptGradingTemplate,storyCreationTemplate,scenesCreationTemplate

model = "meta-llama/llama-4-maverick-17b-128e-instruct"
## Uses's Prompt Grading Chain
usersPromptGrader = ChatGroq(model=model).with_structured_output(GradeUserPrompt)
usersPromptGradingChain = usersPromptGradingTemplate | usersPromptGrader

## Story Creation Chain 
storyCreator = ChatGroq(model=model).with_structured_output(Story)
storyCreationChain = storyCreationTemplate | storyCreator

## Scenes Creation Chain
scenesCreator = ChatGroq(model=model).with_structured_output(Scenes)
scenesCreationChain = scenesCreationTemplate | scenesCreator

