from keras import models
from keras.preprocessing import image
import numpy as np

classifiers: list[str] = ["Meeseeks", "Morty", "Rick", "Summer"]


def classify_image(path: str) -> str:
    model = models.load_model("model.h5")
    return evaluate_image(model, path)


# Evaluate the trained model
def evaluate_image(model, img_path: str) -> str:
    img = image.load_img(img_path, target_size=(250, 250))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_batch)
    prediction_list: list[float] = list(prediction[0])
    index: int = prediction_list.index(max(prediction_list))
    return classifiers[index]


if __name__ == "__main__":
    main()
