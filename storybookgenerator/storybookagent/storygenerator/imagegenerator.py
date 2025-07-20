from together import Together
from PIL import Image
import requests
import os
from dotenv import load_dotenv
import base64
import os

load_dotenv()

# Initialize Together client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def generateImage(prompt: str, filepath: str, filename: str, inference_steps: int = 4):
    response = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=inference_steps,
        width=1024,
        height=768,
        response_format="b64_json",  # <-- key change here
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
