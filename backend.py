from transformers import pipeline
from PIL import Image
import os
import shutil

folder = r"D:\Animals"
animal = "cow"
classifier = pipeline("image-classification", model="Falcom/animal-classifier")
images_loc = []


def make_folder(path, folder_name):
    try:
        new_folder_path = os.path.join(path, folder_name)

        os.makedirs(new_folder_path, exist_ok=True)
        success = "The file has been created at " + os.path.join(path, folder_name)
        return success
    except Exception as e:
        return "This folder already exists"


def get_image(directory):
    images = []

    for i, j, k in os.walk(directory):
        for l in k:
            images.append(os.path.join(i, l))

    return images


def move_images(path, foldername, images_list):
    make_folder(path, foldername)
    executed = False
    for i in images_list:
        basename = os.path.basename(i)
        if os.path.exists(os.path.join(path, foldername, basename)):
            if not executed:
                print(f"Files are already on {os.path.join(path, foldername)}")
                executed = True
        else:
            try:
                shutil.move(i, os.path.join(path, foldername))
                print(f"File moved successfully! to {os.path.join(path, foldername)}")
            except shutil.Error as error:
                print("Error moving file:", error)


def animal():
    for i in get_image(folder):

        image = Image.open(i).convert("RGB")
        result = classifier([image])
        label = max(result[0], key=lambda x: x['score'])
        if label['label'] == animal:
            file_name = os.path.basename(i)
            print(f"The filename is {file_name}")
            images_loc.append(i)

# move_images(folder, animal, images_loc)


