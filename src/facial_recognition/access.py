import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import cv2
import os
import numpy as np
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # configuration

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)  # load facenet model

mtcnn = MTCNN(keep_all=True, margin=20, min_face_size=20, device=device)  # load mtcnn for face detection,


#base_path = "/home/ivang/Ivan/Python/pytorch/facenet/resgister_faces"  # database path

#check that register_faces exists
if not os.path.exists('register_faces'):
    print("The register_faces folder does not exist. Please run the registers.py script first.")
    exit(1)
# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Go up three directories: facial_recognition → src → project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# Path to the new folder at the project root level
base_path = os.path.join(project_root, 'register_faces')


wait_time= 300

for attempt in range(3):
   username = input("Enter your username to access: ")  # username request
   user_dir = os.path.join(base_path, username)

   if  os.path.exists(user_dir):  # check if the username isn't registered
        break
   else:
        print("The user is not registered.")
        if attempt < 2:
            print("Please try again. You have",2 - attempt, "attempts left.")
        else:
            print("You have reached the maximum number of attempts. Please wait 5 minutes.")
            time.sleep(wait_time)
            exit

image_path = os.path.join(user_dir, 'registered_face.jpg')  # path of the resgistered image

if not os.path.exists(image_path):  # check if there is a registered image
    print("No registered image found.")
    exit(1)

registered_image = Image.open(image_path)  # open the image with PIL

registered_boxes = mtcnn(registered_image)  # boxes will contain the coordinates of the detected faces

if registered_boxes is None:   # check if any faces were detected
    print("No face was detected in the recorded image.")
    exit(1)

registered_embedding = model(registered_boxes).detach().cpu().numpy() #passes the face images through the FaceNet model to obtain a feature vector


def take_photo_and_show():  #function to take a photo
    cap = cv2.VideoCapture(0)  # open the default camare (0 is the index)
    if not cap.isOpened():
        print("HE CAMARE COULD NOT BE OPEN.")
        return None

    while True:  # Loop for Video Capture
        ret, frame = cap.read()  # ?????
        if not ret:
            print("HE PHOTO COULD NOT BE TAKEN.")
            break

        cv2.imshow('Press "s" to take the photo or "q" to exit', frame)

        # wait for the user to press 's' or 'q'
        key = cv2.waitKey(1)
        if key == ord('s'):
            new_image_path = os.path.join(user_dir, 'login_face.jpg')  # path for the image
            cv2.imwrite(new_image_path, frame)  # load image in the path
            print("Photo saved as:", new_image_path)
            break
        elif key == ord('q'):
            print("Departure canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()  # closed opencv window


take_photo_and_show()   # function call

new_image = Image.open(os.path.join(user_dir, 'login_face.jpg'))  # open the new image

new_boxes = mtcnn(new_image)  #boxes will contain the coordinates of the detected faces

if new_boxes is None:   # check if any faces were detected
    print("No face was detected in the recorded image.")
    exit(1)

new_embedding = model(new_boxes).detach().cpu().numpy()  #passes the face images through the FaceNet model to obtain a feature vector


def compare_embeddings(embedding1, embedding2):  # function to compare embeddings using the euclidean distance
    distance = np.linalg.norm(embedding1 - embedding2)
    return distance

distance = compare_embeddings(registered_embedding[0], new_embedding[0])  # function call

threshold = 0.6  # adjust if necessary

if distance < threshold:
    print("Access granted.")
else:
    print("Access denied. The images do not mach.")
