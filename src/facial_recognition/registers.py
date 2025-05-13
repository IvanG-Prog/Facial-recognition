import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import cv2
import os
import re


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # configuration

    model = InceptionResnetV1(pretrained='casia-webface').eval().to(device)  # load facenet model

    mtcnn = MTCNN(keep_all=True,margin= 20 ,min_face_size=20, device=device)  # load mtcnn for face detection,

    # user dates
    def valid_name_lastname(input_data):
        return bool(re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", input_data))

    def valid_ID(input_data):
        return input_data.isdigit()

    def valid_username(input_data):
        return bool(re.search("[A-Za-z !@#$%^&*()_+]+", input_data)) and bool(re.search("[0-9]", input_data))

    def register():

        first_names= input("Enter your names: ")
        while not valid_name_lastname(first_names):
            print('Error: Names must only contain letters. Please try again.')
            first_names= input('Enter your names: ')

        last_name= input("Enter your last name: ")
        while not valid_name_lastname(last_name):
            print('Error: last names must only contain letters. Please try again.')
            last_name= input("Enter your last name: ")

        identity_card = input("Enter your identy card: ")
        while not valid_ID(identity_card):
            print("ERROR: The ID card must only contain numbers. Please try again.")
            identity_card = input("Enter your identy card: ")

        username = input("Choose a username: ")
        while not valid_username(username):
            print("Error: Username must contain at least one symbol or number. Please try again.")
            username = input("Choose a username: ")

        return  first_names, last_name, identity_card, username

    first_names, last_name, identity_card, username= register()

    # Absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Go up three directories: facial_recognition → src → project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

    # Path to the new folder at the project root level
    base_path = os.path.join(project_root, 'register_faces')

    # Create the folder if it doesn't exist
    os.makedirs(base_path, exist_ok=True)

    if not os.path.exists(base_path):  # check if the folder exists
        os.makedirs(base_path)  # create the folder if it doesn't exist

    user_dir = os.path.join(base_path, username)  # concatenates the path and the username

    while os.path.exists(user_dir):  # check if the name exists
        print('Username not available', username, 'please choose another')
        username= input('Choose a username: ')
        user_dir = os.path.join(base_path, username)

    os.makedirs(user_dir, exist_ok=True)  # Create a folder


    def take_photo_and_show():  # function to take a photo
        cap = cv2.VideoCapture(0)  # open the default camare (0 is the index)

        if not cap.isOpened():  # check if the camere has opened
            print("THE CAMARE COULD NOT BE OPEN.")
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
                filename = os.path.join(user_dir, 'registered_face.jpg')  # path for the image
                cv2.imwrite(filename, frame)  # load image in the path
                print("Photo saved as:", filename)
                break
            elif key == ord('q'):
                print("Departure canceled.")
                break

        cap.release()  # closed the camare
        cv2.destroyAllWindows()  # closed opencv window

    take_photo_and_show()  # function call


    image_path = os.path.join(user_dir, 'registered_face.jpg')  # path

    image = Image.open(image_path)  # open image
    boxes = mtcnn(image)  # boxes will contain the coordinates of the detected faces

    if boxes is not None:  # check if any faces were detected

        img_cropped = mtcnn(image)  # extracts the face
        embeddings = model(img_cropped).detach().cpu().numpy()  #passes the face images through the FaceNet model to obtain a feature vector

        for i in embeddings:  #for i, embedding in enumerate(embeddings):

            print('Feature vector guardado en', image_path) #print('Feature vector' ,i + 1 , 'guardado en', image_path)
            print(i)
    else:
        print("No face was detected.")


    data_file_path = os.path.join(user_dir, 'user_data.txt')  # created a text file to save the data

    with open(data_file_path, 'w') as data_file:
        data_file.write("Name: " + first_names)
        data_file.write("Last name: " + last_name)
        data_file.write("Identity card: " + identity_card)
        data_file.write("Username: " +   username)

    print("Username data saved in: ", data_file_path)
    print("Registration completed")


if __name__ == "__main__":
    main()


