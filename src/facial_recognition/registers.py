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
import os

import numpy as np

device = torch.device('cpu')  # configuration
# load facenet model
model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)
# load mtcnn for face detection,
mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)


# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
 # Go up three directories: facial_recognition → src → project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

base_path = '/app/register_faces'
os.makedirs(base_path, exist_ok=True)


def check_username(username):
    user_dir = os.path.join(base_path,username)
    return not os.path.exists(user_dir)

def duplicate_face(new_embedding, base_path,threshold=0.6 ):
    for user in os.listdir(base_path):
        user_dir = os.path.join(base_path, user)
        data_file = os.path.join(user_dir, 'user_data.txt')
        if os.path.exists(data_file):
            with open (data_file, 'r') as f:
                for x in f:
                    if x.startswith('Embeddings:'):
                        str = x.replace('Embeddings:', '').strip()
                        try:
                            emb_list =eval(str)
                            old_embedding = np.array(emb_list)
                            dist = np.linalg.norm(new_embedding - old_embedding)
                            if dist < threshold:
                                return True
                        except Exception:
                            continue
    return False

def save_data(image, username, identity_card, first_names, last_name):
    """
    Save user data and photo.
    This function checks if the user already exists, validates the input data,
    and saves the user data and photo.
    """

    '''if not valid_name_lastname(first_names):
        return False, "invalid name"

    if not valid_name_lastname(last_name):
        return False, "Invalid Last name"

    if not valid_id(identity_card):
        return False, "Invalid identity card"

    if not valid_username(username):
        return False, "Invalid username"'''

    # Decode the base64 image
    try:
        header, encoded = image.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        temp_path = "/tmp/temp_face.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_bytes)
        new_embedding = process_image(temp_path)

        if duplicate_face(new_embedding, base_path):
             return False, "A user with this face is already registered."

        user_dir = os.path.join(base_path, username)
        os.makedirs(user_dir, exist_ok= True)
        path = os.path.join(user_dir, 'registered_face.jpg')
        if os.path.exists(path):
            return False, "This username is already registered"

        with open(path, "wb") as f:
            f.write(img_bytes)


        data_file_path = os.path.join(user_dir, 'user_data.txt')
        with open(data_file_path, 'w') as data_file:
            data_file.write("Name: " + first_names + "\n")
            data_file.write("Last name: " + last_name + "\n")
            data_file.write("Identity card: " + identity_card + "\n")
            data_file.write("Username: " + username + "\n")
            data_file.write(f"Embeddings: {new_embedding.tolist()}\n")

        return True, "User successfully registred."
    except Exception as e:
        return False, f"Error: {str(e)}"


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


