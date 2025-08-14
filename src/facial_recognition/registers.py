import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import os
import base64
import numpy as np
import datetime

device = torch.device('cpu')  # configuration

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)  # load facenet model

mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)  # load mtcnn for face detection,


# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
 # Go up three directories: facial_recognition → src → project root


def check_username(username, db_connection):
    user_exists = db_connection.data.find_one({"username": username})
    return user_exists is None

def duplicate_face(new_embedding, db_connection,threshold=0.6 ):
    existing_users = db_connection.data.find({}, {"face_embedding": 1})

    for user_doc in existing_users:
        if "face_embedding" in user_doc and user_doc["face_embedding"] is not None:
            try:
                old_embedding = np.array(user_doc["face_embedding"])
                dist = np.linalg.norm(new_embedding - old_embedding)
                if dist < threshold:
                    return True
            except Exception as e:
                print(f"Error processing MongoDB embedding: {e}")
                continue
    return False

def save_data(image, username, identity_card, first_names, last_name,db_connection ):
    # Decode the base64 image
    try:
        header, encoded = image.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        temp_path = "/tmp/temp_face.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_bytes)

        new_embedding = process_image(temp_path)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        if new_embedding is None:
            return False, "Error: No face vector could be extracted."

        if duplicate_face(new_embedding, db_connection):
             return False, "A user with this face is already registered."

        user_document = {
            "name": first_names,
            "lastname": last_name,
            "id_card": identity_card,
            "username": username,
            "face_embedding": new_embedding.tolist(),
            "registered_at": datetime.datetime.now()
        }

        result = db_connection.data.insert_one(user_document)

        print(f"User '{username}' successfully registered in MongoDB with ID: {result.inserted_id}")
        return True, "User successfully registered and data saved."

    except RuntimeError as re:
            print(f"Image processing error in save_data: {re}")
            return False, f"Image processing error: {re}"

    except Exception as e:
        print(f"General error in save_data: {e}")
        return False, f"An unexpected error occurred during registration: {e}"

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




