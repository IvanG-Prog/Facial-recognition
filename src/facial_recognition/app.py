from flask import Flask, request, jsonify
import registers
import access
import cv2
import base64
import os
import shutil
import numpy as np
from PIL import Image
import io

app= Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Facial Recognition - Cybersecurity</title>
<style>
  body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #00ffe7;
    text-align: center;
  }
  .main-container {
    background: rgba(20, 30, 48, 0.95);
    border-radius: 18px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    padding: 40px 32px 32px 32px;
    width: 370px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1.5px solid #00ffe7;
  }
  h1 {
    font-size: 2.5em;
    margin-bottom: 18px;
    letter-spacing: 1px;
    text-shadow: 0 0 8px #00ffe7aa;
    color: #00ffe7;
  }
  img {
    width: 120px;
    margin-bottom: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 16px #00ffe755;
    border: 2px solid #00ffe7;
  }
  .btn {
    width: 100%;
    padding: 15px 0;
    margin: 10px 0;
    font-size: 1.2em;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s, color 0.3s;
    background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%);
    color: #181f2a;
    font-weight: bold;
    box-shadow: 0 2px 8px #00ffe744;
    letter-spacing: 1px;
  }
  .btn:hover {
    background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%);
    color: #fff;
  }
  .footer {
    margin-top: 18px;
    color: #00ffe7aa;
    font-size: 0.95em;
    letter-spacing: 1px;
  }
</style>
</head>
<body>
  <div class="main-container">
    <img src="https://images.unsplash.com/photo-1506368265446-e4dcbd427a91?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Logo" />
    <h1>Cybersecurity Facial Recognition</h1>
    <button class="btn" onclick="window.location.href='/register'">Register</button>
    <button class="btn" onclick="window.location.href='/access'">Access</button>
    <div class="footer">© 2025 Cybersecurity Facial System</div>
  </div>
</body>
</html>
    '''

@app.route('/check_username', methods=['POST'])
def check_username_endpoint():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'available': False, 'message': "No username provided"}), 400

    ok = registers.check_username(username)
    if ok :
        return jsonify({"available": True, "message": "Username is available"}), 200
    else:
       return jsonify({"available": False, "message": "Username already exists"}), 400


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return r'''
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8" />
        <title>User registration - Cybersecurity Facial</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
                min-height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .registro-container {
                background: rgba(20, 30, 48, 0.95);
                border-radius: 18px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                padding: 40px 32px 32px 32px;
                width: 350px;
                display: flex;
                flex-direction: column;
                align-items: center;
                border: 1.5px solid #00ffe7;
            }
            .registro-container h2 {
                color: #00ffe7;
                margin-bottom: 18px;
                letter-spacing: 1px;
                text-shadow: 0 0 8px #00ffe7aa;
            }
            .registro-container input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
                background: #232b3a;
                color: #00ffe7;
                font-size: 1em;
                outline: none;
                box-shadow: 0 0 0 1.5px #00ffe733;
                transition: box-shadow 0.2s;
            }
            .registro-container input:focus {
                box-shadow: 0 0 0 2.5px #00ffe7;
            }
            .registro-container button {
                width: 100%;
                padding: 14px;
                margin-top: 16px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%);
                color: #181f2a;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 2px 8px #00ffe744;
                letter-spacing: 1px;
                transition: background 0.2s, color 0.2s;
            }
            .registro-container button:hover {
                background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%);
                color: #fff;
            }
            #video {
                margin-top: 18px;
                border-radius: 10px;
                box-shadow: 0 4px 16px #00ffe755;
                border: 2px solid #00ffe7;
                display: none;
            }
            #msg {
                color: #00ffe7;
                margin-top: 10px;
                font-size: 1em;
                text-shadow: 0 0 6px #00ffe7aa;
            }
        </style>
        </head>
        <body>
            <div class="registro-container">
                <h2>Safe Registration</h2>
                <form id="registroForm" autocomplete="off">
                    <input name="name" placeholder="Name" required>
                    <input name="lastname" placeholder="Last Name" required>
                    <input name="id" placeholder="SSNN" required>
                    <input name="username" placeholder="Username" required>
                    <button type="button" onclick="validateAndActivate()">Activate camera</button>
                </form>
                <video id="video" width="320" height="240" autoplay></video>
                <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
                <p id="msg"></p>
            </div>
        <script>
        let streamActive = false;
        function startCamera() {
            const video = document.getElementById('video');
            video.style.display = 'block';
            navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                streamActive = true;
                document.getElementById('msg').innerText = "Press Enter to take the photo and register.";
            })
            .catch(function(err) {
                alert('The camera could not be accessed: ' + err);
            });
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                if (streamActive) {
                    event.preventDefault();
                    takePhotoAndRecord();
                }
            }
        });

        function validateAndActivate() {
    const form = document.getElementById('registroForm');

    const name = form.name.value.trim();
    const lastName = form.lastname.value.trim();
    const id = form.id.value.trim();
    const username = form.username.value.trim();

    // Check for empty fields first
    if (!name || !lastName || !id || !username) {
        alert("Please fill in all fields before activating the camera.");
        return;
    }

    // Validations:
    const numbersOnly = /^\d+$/;
    const lettersAndSpaces = /^[A-Za-z\s]+$/;
    const validUsername = /^[A-Za-z0-9!@#\$%\^&\*\-_\+=\{\}\[\]\(\)\|\\:;'<>,\.\?\/]+$/;

    if (!name.match(lettersAndSpaces)) {
        alert("Name must contain only letters and spaces.");
        return;
    }

    if (!lastName.match(lettersAndSpaces)) {
        alert("Last name must contain only letters and spaces.");
        return;
    }

    if (!id.match(numbersOnly)) {
        alert("ID must contain only numbers.");
        return;
    }

    if (!username.match(validUsername)) {
        alert("Username can contain letters, numbers, and allowed special characters.");
        return;
    }

    fetch('/check_username', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.available) {
            startCamera();
        } else {
            alert(data.message);
        }
    })
    .catch(err => alert('Error checking username: ' + err));
}

        function takePhotoAndRecord() {
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imagenBase64 = canvas.toDataURL('image/png');
            register(imagenBase64);
        }

        function register(imagenBase64) {
            const form = document.getElementById('registroForm');
            if (!form.name.value || !form.lastname.value || !form.id.value || !form.username.value) {
                alert('Please fill in all fields before taking the photo.');
                return;
            }
            const datos = {
                name: form.name.value,
                "last name": form.lastname.value,
                id: form.id.value,
                username: form.username.value,
                image: imagenBase64
            };
            fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(datos)
            }).then(response => response.json())
            .then(data => {
                alert(data.message);
                const video = document.getElementById('video');
                if (video && video.srcObject) {
                    let tracks = video.srcObject.getTracks();
                    tracks.forEach(track => track.stop());
                    video.srcObject = null;
                }
                if (data.status === "ok" || data.status === "face_exists") {
                    console.log("Redirecting now...");
                    window.location.href = "/";
                }
            })
            .catch(err => alert('Error: ' + err));
        }
        </script>
        </body>
        </html>
    '''
    elif request.method == 'POST':

        datos = request.get_json()
        name = datos.get('name')
        lastname = datos.get('last name')
        id_card = datos.get('id')
        username = datos.get('username')
        image = datos.get('image')


        # Call save image funtion
        ok, result =  registers.save_data(image, username, id_card, name, lastname)
        if ok :
            return jsonify({"status": "ok", "message": result}), 200

        else:
            if "face" in result.lower() and "register" in result.lower():
                return jsonify({"status": "face_exists", "message":result}), 200
            print("REGISTER ERROR:", result)
            return jsonify({"status": "error", "message": result}), 400

@app.route('/validate_user', methods=['POST'])
def validate_user():
    data = request.get_json()
    username = data.get('username')
    ssnn = data.get('ssnn')
    if not username or not ssnn:
        return jsonify({"status": "error", "message": "Missing username or SSNN"}), 400

    registred_ssnn = access.get_ssnn_registred(username)
    if not registred_ssnn:
        return jsonify({"status": "error", "message": "User not found"}), 404
    if ssnn != registred_ssnn:
        return jsonify({"status": "error", "message": "SSNN does not match"}), 401

    return jsonify({"status": "ok", "message": "User and SSNN validated"}), 200


@app.route('/access', methods=['GET', 'POST'])
def access_page():
    if request.method == 'GET':
        return r'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <title>User Access - Cybersecurity Facial</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
                min-height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .access-container {
                background: rgba(20, 30, 48, 0.95);
                border-radius: 18px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                padding: 40px 32px 32px 32px;
                width: 350px;
                display: flex;
                flex-direction: column;
                align-items: center;
                border: 1.5px solid #00ffe7;
            }
            .access-container h2 {
                color: #00ffe7;
                margin-bottom: 18px;
                letter-spacing: 1px;
                text-shadow: 0 0 8px #00ffe7aa;
            }
            .access-container input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
                background: #232b3a;
                color: #00ffe7;
                font-size: 1em;
                outline: none;
                box-shadow: 0 0 0 1.5px #00ffe733;
                transition: box-shadow 0.2s;
            }
            .access-container input:focus {
                box-shadow: 0 0 0 2.5px #00ffe7;
            }
            .access-container button {
                width: 100%;
                padding: 14px;
                margin-top: 16px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%);
                color: #181f2a;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 2px 8px #00ffe744;
                letter-spacing: 1px;
                transition: background 0.2s, color 0.2s;
            }
            .access-container button:hover {
                background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%);
                color: #fff;
            }
            #video {
                margin-top: 18px;
                border-radius: 10px;
                box-shadow: 0 4px 16px #00ffe755;
                border: 2px solid #00ffe7;
                display: none;
            }
            #msg {
                color: #00ffe7;
                margin-top: 10px;
                font-size: 1em;
                text-shadow: 0 0 6px #00ffe7aa;
            }
        </style>
        </head>
        <body>
            <div class="access-container">
                <h2>Secure Access</h2>
                <form id="accessForm" autocomplete="off">
                    <input name="username" placeholder="Username" required>
                    <input name="ssnn" placeholder="SSNN" required>
                    <button type="button" onclick="validateAndStartCamera()">Activate camera</button>
                </form>
                <video id="video" width="320" height="240" autoplay></video>
                <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
                <p id="msg"></p>
            </div>
        <script>
        function validateAndStartCamera() {
            const form = document.getElementById('accessForm');
            const username = form.username.value.trim();
            const ssnn = form.ssnn.value.trim();

            if (!username || !ssnn) {
                alert("Please fill in both Username and SSNN before activating the camera.");
                return;
            }

            const numbersOnly = /^\d+$/;
            if (!ssnn.match(numbersOnly)) {
                alert("SSNN must contain only numbers.");
                return;
            }
            fetch('/validate_user', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: username, ssnn: ssnn})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "ok") {
                    startCamera();
                } else {
                    alert(data.message);
                }
            })
            .catch(err => alert('Error: ' + err));

}

        let streamActive = false;
        function startCamera() {
            const video = document.getElementById('video');
            video.style.display = 'block';
            navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                streamActive = true;
                document.getElementById('msg').innerText = "Press Enter to take the photo and access.";
            })
            .catch(function(err) {
                alert('The camera could not be accessed: ' + err);
            });
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                if (streamActive) {
                    takePhotoAndAccess();
                }
            }
        });

        function takePhotoAndAccess() {
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageBase64 = canvas.toDataURL('image/png');
            access(imageBase64);
        }

        function access(imageBase64) {
            const form = document.getElementById('accessForm');
            if (!form.username.value || !form.ssnn.value) {
                alert('Please enter your username and SSNN before taking the photo.');
                return;
            }
            const data = {
                username: form.username.value,
                ssnn: form.ssnn.value,
                image: imageBase64
            };
            fetch('/access', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.status === "ok") {
                    window.location.href = "/documents";
                }
            })
            .catch(err => alert('Error: ' + err));
        }
        </script>
        </body>
        </html>
            '''

    elif request.method == 'POST':

        data = request.get_json()
        username = data.get('username')
        ssnn = data.get('ssnn')
        image_b64 = data.get('image')

        required = [username, ssnn, image_b64]
        if not all(required):
            return jsonify({"status": "error", "message": "Missing data in the form"}), 400

        resgistred_ssnn = access.get_ssnn_registred(username)
        if not resgistred_ssnn:
            return jsonify({"status": "error", "message": "User not found"}), 404
        if ssnn != resgistred_ssnn:
            return jsonify({"status": "error", "message": "SSNN does not match"}), 401


        ok, result= access.access_save(username, image_b64)
        if not ok:
            return jsonify({"status": "error", "message": result}), 400

        success, message = access.compare_face(username, result)
        if success:
            return jsonify({"status": "ok", "message": message}), 200
        else:
            return jsonify({"status": "error", "message": message}), 401







@app.route('/documents')
def documents_page():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Your Documents - Cybersecurity Facial</title>
<style>
  body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #00ffe7;
    text-align: center;
  }
  .main-container {
    background: rgba(20, 30, 48, 0.95);
    border-radius: 18px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    padding: 40px 32px 32px 32px;
    width: 370px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1.5px solid #00ffe7;
  }
  h1 {
    font-size: 2.2em;
    margin-bottom: 18px;
    letter-spacing: 1px;
    text-shadow: 0 0 8px #00ffe7aa;
    color: #00ffe7;
  }
  .doc-list {
    color: #fff;
    margin-top: 20px;
    font-size: 1.1em;
    text-align: left;
  }
  .footer {
    margin-top: 18px;
    color: #00ffe7aa;
    font-size: 0.95em;
    letter-spacing: 1px;
  }
  .btn-logout {
    width: 100%;
    padding: 14px 0;
    margin-top: 24px;
    font-size: 1.1em;
    border: none;
    border-radius: 8px;
    background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%);
    color: #181f2a;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 2px 8px #00ffe744;
    letter-spacing: 1px;
    transition: background 0.2s, color 0.2s;
  }
  .btn-logout:hover {
    background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%);
    color: #fff;
  }
</style>
</head>
<body>
  <div class="main-container">
    <h1>Welcome! Your Documents</h1>
    <div class="doc-list">
      <ul>
        <li>Document 1.pdf</li>
        <li>Document 2.pdf</li>
        <li>Document 3.pdf</li>
      </ul>
    </div>
    <button class="btn-logout" onclick="window.location.href='/'">Logout</button>
    <div class="footer">© 2025 Cybersecurity Facial System</div>
  </div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
