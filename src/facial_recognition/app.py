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

@app.route('/register')
def register_page():
    return '''
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
            <input name="id" placeholder="ID" required>
            <input name="username" placeholder="Username" required>
            <button type="button" onclick="startCamera()">Activate camera</button>
        </form>
        <video id="video" width="320" height="240" autoplay></video>
        <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
        <p id="msg"></p>
    </div>
<script>
let streamActivo = false;
function startCamera() {
    const video = document.getElementById('video');
    video.style.display = 'block';
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        video.srcObject = stream;
        streamActivo = true;
        document.getElementById('msg').innerText = "Press S to take the photo and register.";
      })
      .catch(function(err) {
        alert('The camera could not be accessed: ' + err);
      });
}

document.addEventListener('keydown', function(event) {
    if (event.key === 's' || event.key === 'S') {
        if (streamActivo) {
            takePhotoAndRecord();
        }
    }
});

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
        if (data.status === "ok") {
            window.location.href = "/";
        }
    })
    .catch(err => alert('Error: ' + err));
}
</script>
</body>
</html>
    '''

# Endpoint para procesar registro
@app.route('/register', methods=['POST'])
def register():
    datos = request.get_json()
    name = datos.get('name')
    lastname = datos.get('last name')
    id_card = datos.get('id')
    username = datos.get('username')
    image = datos.get('image')

    #Data validation
    required = [name, lastname, id_card, username, image]
    if not all(required):
        return jsonify({"status": "error", "message": "Missing data in the form"}), 400

    # Temporarily save the image in base_path
    try:
        header, encoded = image.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        os.makedirs(registers.base_path, exist_ok=True)
        temp_img_path = os.path.join(registers.base_path, f"{username}_{id_card}.png")
        with open(temp_img_path, "wb") as f:
            f.write(img_bytes)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving image: {str(e)}"}), 400

    # Call your logging function ONLY with the arguments it expects
    try:
        success, message = registers.register(name, lastname, id_card, username, registers.base_path)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error in registration: {str(e)}"}), 400

    return jsonify({"status": "ok" if success else "error", "message": message}), 200 if success else 400


@app.route('/access')
def access_page():
    return '''
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
            <button type="button" onclick="startCamera()">Activate camera</button>
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
        document.getElementById('msg').innerText = "Press S to take the photo and access.";
      })
      .catch(function(err) {
        alert('The camera could not be accessed: ' + err);
      });
}

document.addEventListener('keydown', function(event) {
    if (event.key === 's' || event.key === 'S') {
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
    if (!form.username.value) {
        alert('Please enter your username before taking the photo.');
        return;
    }
    const data = {
        username: form.username.value,
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

# Endpoint para procesar acceso
@app.route('/access', methods=['POST'])
def access_user():
    data = request.get_json()
    username = data.get('username')
    image_b64 = data.get('image')

    # Paths
    user_dir = os.path.join(registers.base_path, username)
    registered_img_path = os.path.join(user_dir, 'registered_face.jpg')
    login_img_path = os.path.join(user_dir, 'login_face.jpg')

    # Validations
    if not os.path.exists(user_dir):
        return jsonify({"status": "error", "message": "User not registered."}), 400
    if not os.path.exists(registered_img_path):
        return jsonify({"status": "error", "message": "No registered image found."}), 400

    # Save the received image as login_face.jpg
    try:
        header, encoded = image_b64.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        with open(login_img_path, "wb") as f:
            f.write(img_bytes)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving login image: {str(e)}"}), 400

    # Load models (reuse your registers.py logic)
    device = registers.device
    model = registers.model
    mtcnn = registers.mtcnn

    # Helper to get embedding
    def get_embedding(img_path):
        image = Image.open(img_path)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        boxes = mtcnn(image)
        if boxes is None:
            raise RuntimeError("No face detected.")
        embedding = model(boxes).detach().cpu().numpy()
        return embedding[0]

    # Get embeddings
    try:
        registered_embedding = get_embedding(registered_img_path)
        login_embedding = get_embedding(login_img_path)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    # Compare embeddings
    distance = np.linalg.norm(registered_embedding - login_embedding)
    threshold = 0.6  # Adjust as needed

    if distance < threshold:
        return jsonify({"status": "ok", "message": "Access granted."}), 200
    else:
        return jsonify({"status": "error", "message": "Access denied. Face does not match."}), 401


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
    <div class="footer">© 2025 Cybersecurity Facial System</div>
  </div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
