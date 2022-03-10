from keras import models
from keras.preprocessing import image
import numpy as np

classifiers: list[str] = ["meeseeks", "morty", "rick", "summer"]


def classify_image():
    model = models.load_model("model.h5")

    evaluate_image(model, r"test/train/morty/00000000.png")
    evaluate_image(model, r"test/train/meeseeks/00000000.jpg")
    evaluate_image(model, r"test/train/rick/00000000.jpg")
    evaluate_image(model, r"test/train/summer/00000000.jpg")


# Evaluate the trained model
def evaluate_image(model, img_path: str):
    img = image.load_img(img_path, target_size=(250, 250))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_batch)
    prediction_list: list[float] = list(prediction[0])
    index: int = prediction_list.index(max(prediction_list))
    return classifiers[index]


if __name__ == "__main__":
    main()
