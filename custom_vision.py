from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from os import environ


def classify_image_azure(filename, ai_image_results):
    prediction_endpoint: str = environ['prediction_endpoint']
    prediction_key: str = environ['prediction_key']
    project_id: str = environ['project_id']
    model_name: str = environ['model_name']

    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    prediction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=prediction_credentials)

    with open(filename, mode="rb") as image_data:
        results = prediction_client.classify_image(project_id, model_name, image_data)
    ai_image_results.azure_class = results.predictions[0].tag_name
