"""
This module is a Flask application that provides a web interface for facial recognition
registration and access control.
"""
from flask import Flask, redirect, request, jsonify, send_from_directory, url_for
import facial_recognition.registers as registers
import facial_recognition.access as access
import psutil
import os

app= Flask(__name__)




process = psutil.Process(os.getpid())
print(f"Memory used: {process.memory_info().rss / (1024 * 1024):.2f} MB")

# ...resto de tu código Flask...

@app.route('/')
def index():
    """
    Render the main page with options to register or access.
    """
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../facial-frontend'))
    return send_from_directory(os.path.join(frontend_path), 'index.html')

#-------------------------------------------------------
@app.route('/assets/<path:filename>')
def assets(filename):
    frontend_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../facial-frontend/assets'))
    return send_from_directory(frontend_assets, filename)

@app.route('/register.html')
def register_html():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../facial-frontend'))
    return send_from_directory(frontend_path, 'register.html')

@app.route('/access.html')
def access_html():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../facial-frontend'))
    return send_from_directory(frontend_path, 'access.html')

@app.route('/documents.html')
def documents_html():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../facial-frontend'))
    return send_from_directory(frontend_path, 'documents.html')

#------------------------------------------------------


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

#-------------------------------------------------------


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

#------------------------------------------------------------


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

#------------------------------------------------------------


@app.route('/access', methods=['GET', 'POST'])
def access_page():
    """
    Render the access page for users to authenticate using facial recognition.
    """
    if request.method == 'GET':
        return r'''

            '''

    if request.method == 'POST':

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
        return jsonify({"status": "error", "message": message}), 401

#------------------------------------------------------------


@app.route('/documents')
def documents_page():
    """
    Render the documents page for authenticated users.
    """
    return redirect(url_for('documents_html'))



if __name__ == '__main__':
    app.run(debug=True)
