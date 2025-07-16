"""
This module provides functions to register a new user with their personal data and photo.
It includes functions to validate user data, save the user's photo,
and process the photo to obtain face embeddings.
"""
import os
import base64
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import numpy as np


device = torch.device('cpu')

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)

mtcnn = MTCNN(keep_all=True, margin=20, min_face_size=20, device=device)

# Adjust this path according to your structure
current_file_path = os.path.abspath(__file__)

project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

base_path = os.path.join(project_root, 'register_faces')

def get_ssnn_registred(username):
    user_dir = os.path.join(base_path, username)
    user_data = os.path.join(user_dir, 'user_data.txt')
    if not  os.path.exists(user_data):
        return None
    with open(user_data, 'r') as f:
        for line in f:
            if line.startswith('Identity card:'):
                return line.replace('Identity card:', "").strip()

    return None


def access_save(username, image):
    """
    Save the login image for the user and check if the user is registered.
    This function decodes the base64 image, saves it to the user's directory,
    and returns the path of the saved image.
    """


    try:
        user_dir = os.path.join(base_path, username)
        login_image_path = os.path.join(user_dir, 'login_face.jpg')  # path of the login image
        if not os.path.exists(user_dir):
            return False, "User not registered."
        _, encoded = image.split(",", 1)
        image_bytes =   base64.b64decode(encoded)

        with open(login_image_path,'wb') as f:
            f.write(image_bytes)
            return True, login_image_path
    except Exception as e:
        return False, f"Error: {str(e)}"


    #take_photo_and_show(user_dir)   # function call



def compare_face(username, login_image_path, threshold=0.6):
    """
    Compare the face in the login image with the registered face of the user.
    This function checks if the user is registered, processes the images,
    and compares the face embeddings to determine access.
    """
    user_dir = os.path.join(base_path, username)
    registered_image_path = os.path.join(user_dir, 'registered_face.jpg')

    if not os.path.exists(user_dir):
        return False, "User is not registered."
    if not os.path.exists(registered_image_path):
        return False, "No registered image found."

    # Process recorded image
    registered_image = Image.open(registered_image_path)
    if registered_image.mode == 'RGBA':
        registered_image = registered_image.convert('RGB')
    registered_boxes = mtcnn(registered_image)
    if registered_boxes is None:
        return False, "No face detected in registered image."
    registered_embedding = model(registered_boxes).detach().cpu().numpy()[0]

    # Process access image
    login_image = Image.open(login_image_path)
    if login_image.mode == 'RGBA':
        login_image = login_image.convert('RGB')
    login_boxes = mtcnn(login_image)
    if login_boxes is None:
        return False, "No face detected in login image."
    login_embedding = model(login_boxes).detach().cpu().numpy()[0]

    # Compare embeddings
    distance = np.linalg.norm(registered_embedding - login_embedding)
    if distance < threshold:
        return True, "Access granted."

    return False, "Access denied. The faces do not match."
