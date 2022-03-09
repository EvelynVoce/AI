from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os


def classify_image(filename) -> str:
    prediction_endpoint: str = os.environ['prediction_endpoint']
    prediction_key: str = os.environ['prediction_key']
    project_id: str = os.environ['project_id']
    model_name: str = os.environ['model_name']

    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    prediction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=prediction_credentials)

    with open(filename, mode="rb") as image_data:
        results = prediction_client.classify_image(project_id, model_name, image_data)
    return results.predictions[0].tag_name
