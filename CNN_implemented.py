from keras import models
from keras.preprocessing import image
import numpy as np


classifiers: list[str] = ["The eleventh Doctor", "the tenth Doctor", "the thirteenth Doctor", "the twelfth Doctor"]


def classify_image(path: str, ai_image_results):
    model = models.load_model("model.h5")
    ai_image_results.local_class = evaluate_image(model, path)


# Evaluate the trained model
def evaluate_image(model, img_path: str) -> str:
    img = image.load_img(img_path, target_size=(500, 500))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_batch)
    prediction_list: list[float] = list(prediction[0])
    print(prediction_list)  # Useful for testing to see prediction accuracies
    index: int = prediction_list.index(max(prediction_list))
    return classifiers[index]
