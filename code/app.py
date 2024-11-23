# Starting point of program execution.
# The application receives audio/speech input and generates a dynamic image as the output on the Gradio web app.

import torch
import os
import warnings
import gradio as gr
import numpy as np
from transformers import pipeline
import image_generator
import motion_image_generator

warnings.filterwarnings('ignore')

# Set device
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the ASR pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",  # Small model for efficiency
    chunk_length_s=30,
    device=device,
)

# Directory to save the generated output files
OUTPUT_DIR = "./motion_image/"
#OUTPUT_DIR = os.path.abspath("../data/")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Transcription and Generation Logic
def transcribe(audio):
    try:
        sr, y = audio

        # Convert stereo audio to mono if necessary
        if y.ndim > 1:
            y = y.mean(axis=1)

        # Normalize audio
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        # Perform transcription
        result_text = pipe({"sampling_rate": sr, "raw": y})["text"]

        # Generate static image
        static_image = image_generator.image_creation(result_text)
        if isinstance(static_image, str) and "Error" in static_image:
            return result_text, static_image

        # Prepare the image for dynamic image creation
        encoded_image = "data:image/jpeg;base64," + static_image

        # Generate dynamic image
        dynamic_video = motion_image_generator.create_video(encoded_image)
        if isinstance(dynamic_video, str) and "Error" in dynamic_video:
            return result_text, dynamic_video

        # Save the video file
        output_path = os.path.join(OUTPUT_DIR, "output_video.mp4")
        try:
            with open(output_path, "wb") as video_file:
                video_file.write(dynamic_video)
            return result_text, output_path  # Return text and path for Gradio to display
        except Exception as e:
            return result_text, f"Error saving video: {str(e)}"

    except Exception as e:
        return str(e), "Error during processing"

# Gradio Interface
demo = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(type="numpy"),  # Accept audio input
    outputs=[
        gr.Textbox(label="Transcription"),  # Output transcription text
        gr.Video(label="Generated Image"),  # Output dynamic video
    ],
    title="Speech-to-Dynamic-Image Converter",
    description=(
        "This application converts audio input (speech or sounds) into "
        "a descriptive text transcription it then generates a static image-based "
        "on the transcription, and creates a realistic dynamic image."
    ),
)

# Launch the Gradio app
proxy_prefix = os.environ.get("PROXY_PREFIX")
demo.launch(
    server_name="0.0.0.0",
    share=True,
    server_port=8080,
    root_path=proxy_prefix
)
