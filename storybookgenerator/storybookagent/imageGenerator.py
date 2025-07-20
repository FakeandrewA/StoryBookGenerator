import os # for working with dir
import base64 # for converting b64_json to image

from together import Together # for api calls
from langchain_core.prompts import PromptTemplate # for prompt templating

from dotenv import load_dotenv # for loading environment variables

load_dotenv()

##templates
titleImageGenerationTemplate = PromptTemplate.from_template("""
    create a cover page with image for the title - '{title}' 
    and the one line of the story book is - {oneline}     
                                                                                                             
    make sure:
    -To place this title : '{title}' **ALWAYS INCLUDE THIS TITLE IN THE IMAGE** 
    -Make Sure Texts you create in the image is accurate and not a gibberish so focus more on that
    -Dont Explicitly name things like 'Title of the book' near the title 
""") 

sceneImageGenerationTemplate = PromptTemplate.from_template("""
style_of_the_image : {style}
                                                            
{currentScene}
                                                            
system_message: 
You are a creative AI director who is best at setting the scene from imagination to image.
create the scene mentioned , you will have a context of what happened before and what is the current scene 
- please capture the context of the previous scenes in the current scene if nessasary. 
- Make sure to get scene right with continuity from the characters , previous scenes
- also make sure to generate the image in the {style} style.
                                                            
These are the Characters in the Story:
{characterDescription}

            
Previous Scenes:
{previousScenes}                  

""")

# Initialize Together client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def generateImage(prompt: str, filepath: str, filename: str, inference_steps: int = 4):
    response = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=inference_steps,
        width=1024,
        height=768,
        response_format="b64_json",
    )

    # Extract base64-encoded image
    image_b64 = response.data[0].b64_json

    # Decode base64 string to bytes
    img_data = base64.b64decode(image_b64)

    # Ensure the directory exists
    os.makedirs(filepath, exist_ok=True)

    # Save image locally
    with open(os.path.join(filepath, filename), 'wb') as f:
        f.write(img_data)
