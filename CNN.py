from tensorflow import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np

classifiers: list[str] = ["meeseeks", "morty", "rick", "summer"]


def main():
    # All images will be rescaled by 1./255
    train_datagen = ImageDataGenerator()
    img_folder = 'RickMorty/train'

    # Flow training images in batches of 120 using train_datagen generator
    train_generator = train_datagen.flow_from_directory(
            img_folder,  # This is the source directory for training images
            classes=classifiers,
            target_size=(250, 250),  # All images will be resized to 200x200
            # batch_size=32  # <- Not to be confused with 1 image
    )

    model = keras.Sequential(
        [
            keras.Input(shape=(250, 250, 3)),
            layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(64, activation="relu"),
            layers.Dense(4, activation="sigmoid")
        ]
    )

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_generator, epochs=10, batch_size=128)

    model.save("model.h5")

    evaluate_image(model, r"test/train/morty/00000000.png")
    evaluate_image(model, r"test/train/meeseeks/00000000.jpg")
    evaluate_image(model, r"test/train/rick/00000000.jpg")
    evaluate_image(model, r"test/train/summer/00000000.jpg")


# Evaluate the trained model
def evaluate_image(model, img_path: str):
    img = image.load_img(img_path, target_size=(250, 250))
    img.show()

    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_batch)
    prediction_list: list[float] = list(prediction[0])
    print(prediction_list)
    index = prediction_list.index(max(prediction_list))

    global classifiers
    print(classifiers[index])
    return classifiers[index]


if __name__ == "__main__":
    main()


    # csv_file = 'rick_morty.csv'
    # with open(csv_file, 'r') as f:
    #     reader = csv.reader(f)
    #     rows: dict[str, str] = {line[0]: line[1] for line in reader}  # Loading the dataset
    # class_names = list(rows.keys())
    # print(class_names)



# # A classical NN; adapted from https://www.tensorflow.org/tutorials/keras/classification/
#
# import csv
# from tensorflow import keras, nn
# from keras import layers
# from keras.preprocessing.image import ImageDataGenerator
# import matplotlib.pyplot as plt
# import numpy as np
# # from google.colab import files
# from keras.preprocessing import image
#
#
# def main():
#     csv_file = 'rick_morty.csv'
#     with open(csv_file, 'r') as f:
#         reader = csv.reader(f)
#         rows: dict[str, str] = {line[0]: line[1] for line in reader}  # Loading the dataset
#     class_names = list(rows.keys())
#     print(class_names)
#
#     # All images will be rescaled by 1./255
#     train_datagen = ImageDataGenerator(rescale=1/255)
#     img_folder = 'RickMorty/train'
#     # Flow training images in batches of 120 using train_datagen generator
#     train_generator = train_datagen.flow_from_directory(
#             img_folder,  # This is the source directory for training images
#             classes=class_names,
#             target_size=(200, 200),  # All images will be resized to 200x200
#             batch_size=120
#     )
#
#     model = keras.Sequential(
#         [
#             keras.Input(shape=(200, 200, 3)),
#             layers.Conv2D(32, (3, 3), activation='relu'),
#             layers.MaxPooling2D(pool_size=(2, 2)),
#             layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#             layers.MaxPooling2D(pool_size=(2, 2)),
#             layers.Flatten(),
#             layers.Dropout(0.5),
#             layers.Dense(256, activation="relu"),
#             layers.Dense(5, activation="sigmoid")
#         ]
#     )
#
#     # CNN model
#     # model = keras.models.Sequential([keras.layers.Flatten(input_shape=(200, 200, 3)),
#     #                                  keras.layers.Dense(128, activation=nn.relu),
#     #                                  keras.layers.Dense(1, activation=nn.sigmoid)])
#
#     model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#     model.fit(train_generator, epochs=10, batch_size=128)
#
#     # model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
#     # model.fit(train_generator, epochs=10, batch_size=128)
#
#     # # Google.colab import needed for this however cannot install module on my desktop
#     # uploaded = files.upload()
#     # for fn in uploaded.keys():
#     #     # predicting images
#     #     path = '/content/' + fn
#     #     img = image.load_img(path, target_size=(200, 200))
#     #     x = image.img_to_array(img)
#     #     plt.imshow(x / 255.)
#     #     x = np.expand_dims(x, axis=0)
#     #     images = np.vstack([x])
#     #     classes = model.predict(images, batch_size=10)
#     #     print(classes)
#     #     # print(classes[0])
#     #     # print(fn + " is a dandelion") if classes[0] < 0.5 else print(fn + " is a grass")
#
#     # # Evaluate the trained model
#     # test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
#     # print('\n Test accuracy:', test_acc)
#     # # plt.figure(figsize=(20,20))
#     # test_folder = r'RickMorty'
#     # for i in range(5):
#     #     file = random.choice(os.listdir(test_folder))
#     #     image_path = os.path.join(test_folder, file)
#     #     img=mpimg.imread(image_path)
#     #     ax=plt.subplot(1, 5, i+1)
#     #     ax.title.set_text(file)
#     #     plt.imshow(img)
#
#
# if __name__ == "__main__":
#     main()
