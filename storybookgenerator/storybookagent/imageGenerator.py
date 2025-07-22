import os # for working with dir
import base64 # for converting b64_json to image

from concurrent.futures import ThreadPoolExecutor, TimeoutError

from together import Together # for api calls
from langchain_core.prompts import PromptTemplate # for prompt templating

from dotenv import load_dotenv # for loading environment variables

load_dotenv()

##templates
titleImageGenerationTemplate = PromptTemplate.from_template("""
    {title}                                                                                          
""") 

sceneImageGenerationTemplate = PromptTemplate.from_template("""
                                                   
A {style} image of {currentScene}
                                                                       
""")

# Initialize Together client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def _generate_internal(prompt, inference_steps, width, height):
    response = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=inference_steps,
        width=width,
        height=height,
        response_format="b64_json",
    )
    return response.data[0].b64_json

def generateImage(prompt: str, filepath: str, filename: str, inference_steps: int = 2, width=512, height=384, timeout_seconds=30, max_retries=3):
    os.makedirs(filepath, exist_ok=True)
    retry_count = 0

    while retry_count < max_retries:
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_generate_internal, prompt, inference_steps, width, height)
                image_b64 = future.result(timeout=timeout_seconds)

            img_data = base64.b64decode(image_b64)
            with open(os.path.join(filepath, filename), 'wb') as f:
                f.write(img_data)
            print(f"[✅] Image saved: {filename}")
            break  # Success, exit loop

        except TimeoutError:
            retry_count += 1
            print(f"[⏰] Timeout after {timeout_seconds} seconds. Retrying... ({retry_count}/{max_retries})")

        except Exception as e:
            retry_count += 1
            print(f"[❌] Failed: {e}. Retrying... ({retry_count}/{max_retries})")

    else:
        print("[🚫] Maximum retries exceeded. Image generation falied.")
