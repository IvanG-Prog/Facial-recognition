import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import cv2
import os
import numpy as np
import time


device = torch.device('cpu')
model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)
mtcnn = MTCNN(keep_all=True, margin=20, min_face_size=20, device=device)

# Adjust this path according to your structure
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
base_path = os.path.join(project_root, 'register_faces')

def main():
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

    take_photo_and_show(user_dir)   # function call

    login_image_path = os.path.join(user_dir, 'login_face.jpg')  # path of the login image

    access_granted, message = compare_face(username, login_image_path)
    print(message)

def compare_face(username, login_image_path, threshold=0.6):
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

    # Comparar embeddings
    distance = np.linalg.norm(registered_embedding - login_embedding)
    if distance < threshold:
        return True, "Access granted."
    else:
        return False, "Access denied. The faces do not match."

def take_photo_and_show(user_dir):  #function to take a photo
        cap = cv2.VideoCapture(0)  # open the default camera (0 is the index)
        if not cap.isOpened():
            print("THE CAMERA COULD NOT BE OPEN.")
            return None

        while True:  # Loop for Video Capture
            ret, frame = cap.read()  # ?????
            if not ret:
                print("THE PHOTO COULD NOT BE TAKEN.")
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

if __name__ == "__main__":
    main()
