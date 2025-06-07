import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import cv2
import os
import re
import shutil
import base64
from flask import jsonify
import numpy as np

device = torch.device('cpu')  # configuration

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)  # load facenet model

mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)  # load mtcnn for face detection,


# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
 # Go up three directories: facial_recognition → src → project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Path to the new folder at the project root level
base_path = os.path.join(project_root, 'register_faces')

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
    image = Image.open(image_path)  # open image
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # convert to RGB
    boxes = mtcnn(image)  # boxes will contain the coordinates of the detected faces
    if boxes is None:  # check if any faces were detected
        raise RuntimeError("No face was detected in the photo.")

    embeddings = model(boxes).detach().cpu().numpy()  #passes the face images through the FaceNet model to obtain a feature vector
    return embeddings




''' This funtion will only be used in consola:

def take_photo_and_show(user_dir):  # function to take a photo
    cap = cv2.VideoCapture(0)  # open the default camera (0 is the index)
    if not cap.isOpened():  # check if the camera has opened
         raise RuntimeError("The camera could not be opened.")

    while True:  # Loop for Video Capture
        ret, frame = cap.read()  # ?????
        if not ret:
           cap.release()
           raise RuntimeError("THE PHOTO COULD NOT BE TAKEN..")

        cv2.imshow('Press "s" to take the photo or "q" to exit', frame)

        # wait for the user to press 's' or 'q'
        key = cv2.waitKey(1)
        if key == ord('s'):
            filename = os.path.join(user_dir, 'registered_face.jpg')  # path for the image
            cv2.imwrite(filename, frame)  # load image in the path
            cv2.destroyAllWindows()  # closed opencv window
            cap.release()  # closed the camare
            return filename
        elif key == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                raise RuntimeError("Capture canceled by user")'''




