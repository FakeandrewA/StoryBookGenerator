import os
import base64
import multiprocessing
from dotenv import load_dotenv
from together import Together
from langchain_core.prompts import PromptTemplate

load_dotenv()  # TOGETHER_API_KEY in your .env

# Templates
sceneImageGenerationTemplate = PromptTemplate.from_template(
    "A {style} image of {currentScene}"
)
titleImageGenerationTemplate = PromptTemplate.from_template(
    "{titleImagePrompt}"
)
def _generate_internal(prompt: str, inference_steps: int, width: int, height: int):
    """
    Calls the Together API. Returns base64-encoded image data or raises.
    """
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    if not client:
        raise RuntimeError("Together client init failed")
    resp = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=inference_steps,
        width=width,
        height=height,
        response_format="b64_json",
    )
    if not (resp and getattr(resp, "data", None)):
        raise RuntimeError("No data in response")
    b64 = resp.data[0].b64_json
    if not b64:
        raise RuntimeError("Empty image returned")
    return b64

def generateImage(
    prompt: str,
    filepath: str,
    filename: str,
    inference_steps: int = 2,
    width: int = 512,
    height: int = 384,
    timeout_seconds: int = 15,
    max_retries: int = 3,
):
    os.makedirs(filepath, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        # Create a fresh pool with a single worker each time
        with multiprocessing.Pool(1) as pool:
            async_res = pool.apply_async(
                _generate_internal,
                (prompt, inference_steps, width, height)
            )
            try:
                # This will block only up to timeout_seconds
                b64_data = async_res.get(timeout=timeout_seconds)
            except multiprocessing.TimeoutError:
                print(f"[⏰] Timeout after {timeout_seconds}s. Retrying {attempt}/{max_retries}…")
                pool.terminate()  # kill the worker immediately
                pool.join()
                continue
            except Exception as e:
                print(f"[❌] Generation error ({e}). Retrying {attempt}/{max_retries}…")
                # worker will auto-clean on exiting the with‑block
                continue

            # At this point we have valid b64_data
            try:
                img_bytes = base64.b64decode(b64_data)
                out_path = os.path.join(filepath, filename)
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"[✅] Image saved to {out_path}")
                return
            except Exception as e:
                print(f"[❌] Failed to save image ({e}). Retrying {attempt}/{max_retries}…")
                continue

    print(f"[🚫] All {max_retries} attempts failed. No image generated.")


if __name__ == "__main__":
    prompt = sceneImageGenerationTemplate.format(
        style="Cartoon",
        currentScene="a colorful sunset over snow-capped mountains"
    )
    generateImage(
        prompt=prompt,
        filepath="output_images",
        filename="scene_sunset.png",
        inference_steps=1,
        width=640,
        height=480,
        timeout_seconds=10,
        max_retries=2
    )
