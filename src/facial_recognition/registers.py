"""
This module provides functions to register a new user with their personal data and photo.
It includes functions to validate user data, save the user's photo,
and process the photo to obtain face embeddings.
"""
import os
import re
import base64
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image



device = torch.device('cpu')  # configuration
# load facenet model
model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)
# load mtcnn for face detection,
mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)


# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
 # Go up three directories: facial_recognition → src → project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Path to the new folder at the project root level
base_path = os.path.join(project_root, 'register_faces')


def save_data(image, username, identity_card, first_names, last_name):
    """
    Save user data and photo.
    This function checks if the user already exists, validates the input data,
    and saves the user data and photo.
    """

    if not valid_name_lastname(first_names):
        return False, "invalid name"

    if not valid_name_lastname(last_name):
        return False, "Invalid Last name"

    if not valid_id(identity_card):
        return False, "Invalid identity card"

    if not valid_username(username):
        return False, "Invalid username"

    # Decode the base64 image
    try:
        user_dir = os.path.join(base_path, username)
        os.makedirs(user_dir, exist_ok= True)
        path = os.path.join(user_dir, 'registered_face.jpg')
        if os.path.exists(path):
            return False, "The user already exists."
        _, encoded = image.split(",", 1)
        img_bytes = base64.b64decode(encoded)

        with open(path, "wb") as f:
            f.write(img_bytes)
            return True, path
    except Exception as e:
        return False, f"Error: {str(e)}"


def register(first_names, last_name, identity_card, username, base_path):
    """
    Register a new user.
    This function checks if the user already exists, validates the input data,
    processes the photo to obtain face embeddings, and saves the user data.
    :param first_names: First names of the user.
    :param last_name: Last name of the user.
    :param identity_card: Identity card number of the user.
    :param username: Username of the user.
    :param base_path: Base path where user data will be stored.
    :return: Tuple (success, message) indicating the result of the registration.
    """

    user_dir = os.path.join(base_path, username)
    photo_path = os.path.join(user_dir, 'registered_face.jpg')
    if not os.path.exists(photo_path):
        return False, "The submitted photo was not found."


    # Process the photo and obtain embeddings
    try:
        embeddings = process_image(photo_path)
    except RuntimeError as e:
        return False, str(e)

    # Save data
    # created a text file to save the data
    data_file_path = os.path.join(user_dir, 'user_data.txt')
    with open(data_file_path, 'w', encoding='utf-8') as data_file:
        data_file.write("Name: " + first_names + "\n")
        data_file.write("Last name: " + last_name + "\n")
        data_file.write("Identity card: " + identity_card + "\n")
        data_file.write("Username: " + username + "\n")
        data_file.write(f"Embeddings: {embeddings.tolist()}\n")  # save vector

    return True, "User successfully registered."

 # user dates
def valid_name_lastname(input_data):
    """
    Validate the first name and last name.
    The name must contain only letters (including accented characters) and spaces.
    It should not contain numbers or special characters.
    """
    return bool(re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", input_data))

def valid_id(input_data):
    """
    Validate the identity card number.
    The identity card number must contain only digits.
    """
    return input_data.isdigit()

def valid_username(input_data):
    """
    Validate the username.
    The username must contain at least one letter, one number, and can include special characters.
    """
    return bool(re.search("[A-Za-z !@#$%^&*()_+]+", input_data)) and bool(re.search("[0-9]", input_data))



def process_image(image_path):
    """
    Process the image to obtain face embeddings.
    """
    image = Image.open(image_path)  # open image
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # convert to RGB
    boxes = mtcnn(image)  # boxes will contain the coordinates of the detected faces
    if boxes is None:  # check if any faces were detected
        raise RuntimeError("No face was detected in the photo.")

    # passes the face images through the FaceNet model to obtain a feature vector
    embeddings = model(boxes).detach().cpu().numpy()
    return embeddings
