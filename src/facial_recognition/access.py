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
import os
import numpy as np
import base64
from flask import jsonify



device = torch.device('cpu')

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)

mtcnn = MTCNN(keep_all=True, margin=20, min_face_size=20, device=device)



def get_ssnn_registred(username, db_connection):
    user_data = db_connection.data.find_one({"username": username})

    if user_data:
        return user_data.get("id_card")
    return None

def process_image_access(image_path):
    image = Image.open(image_path)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    boxes, _ = mtcnn.detect(image)
    if boxes is None or len(boxes) == 0:
        raise RuntimeError("No face was detected in the photo.")

    aligned_faces = mtcnn(image)
    if aligned_faces is None or len(aligned_faces) == 0:
        raise RuntimeError("No face was detected or aligned for embedding.")


    embeddings = model(aligned_faces).detach().cpu().numpy()
    return embeddings[0]


def process_access_attempt(image_base64, db_connection):
    try:
        header, encoded = image_base64.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        temp_path = "/tmp/temp_access_face.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_bytes)


        attempt_embedding = process_image_access(temp_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if attempt_embedding is None:
            return None, "Error: No face detected during login attempt."

        return attempt_embedding, "Facial embedding successfully extracted."

    except RuntimeError as re:
        print(f"Error processing access image: {re}")
        return None, f"Error processing access image: {re}"
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el procesamiento del intento de acceso: {e}")
        return None, f"Ocurrió un error inesperado durante el procesamiento del intento de acceso: {e}"



def compare_face(username, attempt_embedding, db_connection, threshold=0.6):
    user_document = db_connection.data.find_one({"username": username})
    if not user_document:

        return False, "User is not registered."

    registered_embedding_list = user_document.get("face_embedding")

    if not registered_embedding_list:
        return False, "No facial embedding was found for this user."
    registered_embedding = np.array(registered_embedding_list)
    distance = np.linalg.norm(registered_embedding - attempt_embedding)
    if distance < threshold:
        return True, "Access granted."
