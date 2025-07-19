from gradio_client import Client
from dotenv import load_dotenv
from PIL import Image
import os
load_dotenv()


client = Client("black-forest-labs/FLUX.1-Schnell",hf_token=os.getenv("HF_TOKEN"))

def generateImage(prompt:str,filepath:str,filename:str,inference_steps:int=10):

    localpath = client.predict(
        prompt = prompt,
        randomize_seed=True,
        num_inference_steps = inference_steps
    )
    image = Image.open(localpath[0])
    os.makedirs(filepath,exist_ok=True)
    image.save(filepath+"/"+filename)