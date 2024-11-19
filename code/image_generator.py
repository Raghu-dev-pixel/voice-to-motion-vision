#This Python code is used to convert text to image using Nvidia's API
import requests
import os
from PIL import Image
from io import BytesIO
import base64
from IPython.display import display


# This function creates a static image using stable-diffusion through Nvidia's API.
def image_creation(text):
    invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

    token = os.environ.get("NVCF_RUN_KEY")
    headers = {
        #"Authorization": "Bearer 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", #Replace with your Nvidia API
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    # Payload with text prompts
    payload = {
        "text_prompts": [
            {
                "text": text,
                "weight": 1
            }
        ],
        "cfg_scale": 5,
        "sampler": "K_DPM_2_ANCESTRAL",
        "seed": 0,
        "steps": 25
    }

    # Send the request
    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()

        # Get the JSON response
        response_body = response.json()

        # Extract the base64 image data and return the base64-encoded image data
        image_data_base64 = response_body['artifacts'][0]['base64']
        return image_data_base64
        
    except requests.exceptions.RequestException as e:
        return f"Error in image creation: {str(e)}"