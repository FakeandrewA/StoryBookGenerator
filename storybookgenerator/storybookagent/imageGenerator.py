import os # for working with dir
import base64 # for converting b64_json to image


from multiprocessing import Process, Queue


from together import Together # for api calls
from langchain_core.prompts import PromptTemplate # for prompt templating

from dotenv import load_dotenv # for loading environment variables

load_dotenv()

##templates
titleImageGenerationTemplate = PromptTemplate.from_template("""
    {titleImagePrompt}                                                                                          
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

def _generate_process(prompt, inference_steps, width, height, queue):
    try:
        b64 = _generate_internal(prompt, inference_steps, width, height)
        queue.put(b64)
    except Exception as e:
        queue.put(e)

def generateImage(prompt: str, filepath: str, filename: str, inference_steps: int = 2, width=512, height=384, timeout_seconds=15, max_retries=3):
    os.makedirs(filepath, exist_ok=True)
    retry_count = 0

    while retry_count < max_retries:
        retry_count += 1
        queue = Queue()
        process = Process(target=_generate_process, args=(prompt, inference_steps, width, height, queue))
        process.start()
        process.join(timeout_seconds)

        if process.is_alive():
            process.terminate()
            print(f"[⏰] Timeout after {timeout_seconds}s. Retrying... ({retry_count}/{max_retries})")
            continue

        result = queue.get()

        if isinstance(result, Exception):
            print(f"[❌] Failed: {result}. Retrying... ({retry_count}/{max_retries})")
            continue

        # Success
        img_data = base64.b64decode(result)
        with open(os.path.join(filepath, filename), 'wb') as f:
            f.write(img_data)
        print(f"[✅] Image saved: {filename}")
        break

    else:
        print("[🚫] Maximum retries exceeded. Image generation failed.")
