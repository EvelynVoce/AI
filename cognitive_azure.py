from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os


def get_caption(description) -> str:
    # Display the image
    caption_text: str = ""
    if len(description.captions) == 0:
        caption_text = 'No caption detected'
    else:
        for caption in description.captions:
            caption_text += f" '{caption.text}'\n(Confidence: {caption.confidence * 100:.2f}%)"
    return caption_text


def connect(image_path: str) -> str:
    cog_key: str = os.environ['cog_key']
    cog_endpoint: str = os.environ['cog_endpoint']

    # Get a client for the computer vision service
    computer_vision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

    # Get a description from the computer vision service
    image_stream = open(image_path, "rb")
    description = computer_vision_client.describe_image_in_stream(image_stream)

    # Display image and caption (code in helper_scripts/vision.py)
    return get_caption(description)
