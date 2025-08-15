"""
This module is a Flask application that provides a web interface for facial recognition
registration and access control.
"""
from flask import Flask, request, jsonify
import facial_recognition.registers as registers
import facial_recognition.access as access
from flask_cors import CORS
import psutil
import os

app = Flask(__name__)
CORS(app)




process = psutil.Process(os.getpid())
print(f"Memory used: {process.memory_info().rss / (1024 * 1024):.2f} MB")



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
    """
    Render the registration page for new users.
    """
    if request.method == 'GET':
        return r'''

    '''

    if request.method == 'POST':

        datos = request.get_json()
        name = datos.get('name')
        lastname = datos.get('last name')
        id_card = datos.get('id')
        username = datos.get('username')
        image = datos.get('image')


        # Call save image function
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



@app.route('/access', methods=['POST'])
def access_page():
    """
    Authenticate user using facial recognition.
    """
    try:
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

        ok, result = access.access_save(username, image_b64)
        if not ok:
            return jsonify({"status": "error", "message": result}), 400

        success, message = access.compare_face(username, result)
        if success:
            return jsonify({"status": "ok", "message": message}), 200
        return jsonify({"status": "error", "message": message}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
