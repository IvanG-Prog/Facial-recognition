import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import cv2
import os
import re
import shutil

device = torch.device('cpu')  # configuration

model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)  # load facenet model

mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)  # load mtcnn for face detection,


# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
 # Go up three directories: facial_recognition → src → project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Path to the new folder at the project root level
base_path = os.path.join(project_root, 'register_faces')


    # user dates
def valid_name_lastname(input_data):
    return bool(re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", input_data))

def valid_ID(input_data):
    return input_data.isdigit()

def valid_username(input_data):
    return bool(re.search("[A-Za-z !@#$%^&*()_+]+", input_data)) and bool(re.search("[0-9]", input_data))

def register(first_names, last_name, identity_card, username, base_path):

        if not valid_name_lastname(first_names):
            return False, "invalid name"

        if not valid_name_lastname(last_name):
            return False, "Invalid Last name"

        if not valid_ID(identity_card):
            return False, "Invalid identity card"

        if not valid_username(username):
            return False, "Invalid username"


        user_dir = os.path.join(base_path, username)
        if os.path.exists(user_dir):
            return False, "The user already exists."

        # Create the folder if it doesn't exist
        os.makedirs(user_dir, exist_ok=True)

        # NO LLAMES a take_photo_and_show
        # foto_path = take_photo_and_show(user_dir)

        # Usa la imagen que ya guardaste en el backend:
        foto_temp = os.path.join(base_path, f"{username}_{identity_card}.png")
        foto_path = os.path.join(user_dir, 'registered_face.jpg')

        if not os.path.exists(foto_temp):
            return False, "No se encontró la foto enviada."

        # Mueve la imagen a la carpeta del usuario
        shutil.move(foto_temp, foto_path)

        # Procesar foto y obtener embedding
        try:
            embeddings = process_image(foto_path)
        except RuntimeError as e:
            return False, str(e)

        # save data
        data_file_path = os.path.join(user_dir, 'user_data.txt')  # created a text file to save the data
        with open(data_file_path, 'w') as data_file:
            data_file.write("Name: " + first_names + "\n")
            data_file.write("Last name: " + last_name + "\n")
            data_file.write("Identity card: " + identity_card + "\n")
            data_file.write("Username: " + username + "\n")
            data_file.write(f"Embeddings: {embeddings.tolist()}\n")  # save vector

        return True, "User successfully registered."

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
                raise RuntimeError("Capture canceled by user")



def process_image(image_path):
    image = Image.open(image_path)  # open image
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # convert to RGB
    boxes = mtcnn(image)  # boxes will contain the coordinates of the detected faces
    if boxes is None:  # check if any faces were detected
        raise RuntimeError("No face was detected in the photo.")

    embeddings = model(boxes).detach().cpu().numpy()  #passes the face images through the FaceNet model to obtain a feature vector
    return embeddings



#if __name__ == "__main__":
   #main()
















#if not os.path.exists(base_path):  # check if the folder exists
        #os.makedirs(base_path)  # create the folder if it doesn't exist
#user_dir = os.path.join(base_path, username)  # concatenates the path and the username


'''while os.path.exists(user_dir):  # check if the name exists
        print('Username not available', username, 'please choose another')
        username= input('Choose a username: ')
        user_dir = os.path.join(base_path, username)

        os.makedirs(user_dir, exist_ok=True)  # Create a folder
image_path = os.path.join(user_dir, 'registered_face.jpg')  # path


    #take_photo_and_show(user_dir)  # function call'''
