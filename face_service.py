from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from os import environ


def get_faces(image_path):
    face_client = FaceClient(environ['face_endpoint'], CognitiveServicesCredentials(environ['face_key']))
    image = open(image_path, 'rb')
    return face_client.face.detect_with_stream(image)


# Convert width height to a point in a rectangle
def get_rectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return (left, top), (right, bottom)


def draw_face_rectangles(image_path: str, detected_faces):
    # For each face returned use the face rectangle and draw a red box.
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    for face in detected_faces:
        draw.rectangle(get_rectangle(face), outline='red')
    image.show()


def face_recognition(path: str):
    detected_faces = get_faces(path)
    draw_face_rectangles(path, detected_faces)
