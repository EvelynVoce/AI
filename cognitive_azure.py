from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from os import environ


def get_caption(description) -> str:
    captions: list[str] = description.captions
    return f"I am {captions[0].confidence * 100:.2f}% certain that this is {captions[0].text}" if captions else "No caption detected"


def get_description(image_path: str) -> str:
    cog_key: str = environ['cog_key']
    cog_endpoint: str = environ['cog_endpoint']

    # Get a client for the computer vision service
    computer_vision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

    image_stream = open(image_path, "rb")
    description = computer_vision_client.describe_image_in_stream(image_stream)
    return get_caption(description)
