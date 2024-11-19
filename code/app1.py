# Starting point of program execution.
## The application receives audio/speech input and generates a dynamic image as the output on the gradio web app


import torch
import os
import warnings
import gradio as gr
import numpy as np
from IPython.display import display
from transformers import pipeline
import image_generator
import motion_image_generator

warnings.filterwarnings('ignore')
# Set device
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the ASR pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    #model="openai/whisper-large",
    model="openai/whisper-small",
    chunk_length_s=30,
    device=device,
)

def transcribe(audio):
    try:
        sr, y = audio
    
        # Convert to mono if stereo
        if y.ndim > 1:
            y = y.mean(axis=1)
        
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        result_text = pipe({"sampling_rate": sr, "raw": y})["text"]
        
        #Get the static image from the audio input
        image = image_generator.image_creation(result_text)
        
        #Return the error message, if the static image creation is unsuccessful
        if "Error" in image:
            return result_text, image

        encoded_image = "data:image/jpeg;base64," + image

        #Get the dynamic image from encrypted image input
        dynamic_image = motion_image_generator.create_video(encoded_image)

        #Return the error message, if the static image creation is unsuccessful
        if isinstance(dynamic_image, str) and "Error" in video_data:
            return result_text, dynamic_image

        output_path = "./data/images/output_video.mp4"

        # Save the video binary data to a file
        try:
            with open(output_path, "wb") as video_file:
                video_file.write(dynamic_image)
            return result_text, output_path  # Return the file path to be used by Gradio
        except Exception as e:
            return f"Error saving video: {str(e)}"
        
        #return result_text
    except Exception as e:
        return str(e)

demo = gr.Interface(
    transcribe,
    #gr.Audio(sources="microphone"),
    inputs=gr.Audio(type="numpy"),
    #outputs="text",
    outputs=[gr.Textbox(label="Transcription"),gr.Video(label="Image")],
    title="Speech to Image Conversion Application",
)

proxy_prefix = os.environ.get("PROXY_PREFIX")
demo.launch(server_name="0.0.0.0", share=True,server_port=8080, root_path=proxy_prefix)
#demo.launch(share=True)