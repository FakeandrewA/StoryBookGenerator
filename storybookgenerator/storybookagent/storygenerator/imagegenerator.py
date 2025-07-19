# from gradio_client import Client
# from dotenv import load_dotenv
# from PIL import Image
# import os
# load_dotenv()

# client = Client("black-forest-labs/FLUX.1-Schnell",hf_token=os.getenv("HF_TOKEN"))

# def generateImage(prompt:str,filepath:str,filename:str,inference_steps:int=10):

#     localpath = client.predict(
#         prompt = prompt,
#         randomize_seed=True,
#         num_inference_steps = inference_steps
#     )
#     image = Image.open(localpath[0])
#     os.makedirs(filepath,exist_ok=True)
#     image.save(filepath+"/"+filename)

from together import Together
from PIL import Image
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Together client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def generateImage(prompt: str, filepath: str, filename: str, inference_steps: int = 4):
    # Send prompt to Together AI's FLUX.1-Schnell model
    response = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=inference_steps,
        width=1024,
        height=768,
        response_format="url",
    )

    # Extract the image URL from response
    image_url = response.data[0].url

    # Download the image
    img_data = requests.get(image_url).content

    # Ensure the directory exists
    os.makedirs(filepath, exist_ok=True)

    # Save image locally
    with open(os.path.join(filepath, filename), 'wb') as f:
        f.write(img_data)
