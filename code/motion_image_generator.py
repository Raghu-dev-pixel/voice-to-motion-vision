import requests
import base64
import os

# This function creates a dynamic image using stable-video-diffusion through Nvidia's API.
def create_video(load):
    invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

    token = os.environ.get("NVCF_RUN_KEY")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    payload = {
      "image": load,
      "cfg_scale": 2.5,
      "seed": 0
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        response_body = response.json()
        video_data_base64 = response_body['video']
        #Decode and return the video binary data
        video_data = base64.b64decode(video_data_base64)
        return video_data
    except requests.exceptions.RequestException as e:
        return f"Error in video creation: {str(e)}" #return error if there are any exceptions
