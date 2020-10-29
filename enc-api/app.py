from flask import Flask, render_template, jsonify, request, make_response
from cryptography.fernet import Fernet
from os import path

app = Flask(__name__)

_enc_key_path = 'enc.key'


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    if not path.exists(_enc_key_path):
        with open(_enc_key_path, "wb") as key_file:
            key_file.write(key)


def load_key():
    """
    Loads the key named enc.key from the current directory.
    """
    generate_key()
    return open(_enc_key_path, "rb").read()


@app.route('/', methods=['GET'])
def main_page():
    """
    This func will serve the default page
    :return:
    """
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """
    This func will serve the health api
    :return:
    """
    data = {'state': 'Healthy'}
    return make_response(jsonify(data), 200)


@app.route('/api/encrypt', methods=['POST', 'GET'])
def encrypt():
    """
    This func will encrypt the given API
    :return: Payload and Status Code
    """

    try:
        key = load_key()
        data = request.json
        if data.get('Input') and len(data.get('Input')):
            encoded_message = data.get('Input').encode()
            print(encoded_message)
            enc_file = Fernet(key)
            encrypted_message = enc_file.encrypt(encoded_message)
            print(encrypted_message)
            resp = {"input": data.get('Input'), "Output": encrypted_message.decode('utf-8'),
                    "Status": "success", "Message": "Encryption success"}
            return make_response(jsonify(resp), 200)
        else:
            resp = {"input": None, "Output": None, "Status": "Failed", "Message": "Empty Input"}
            return make_response(jsonify(resp), 200)
    except Exception as e:
        resp = {"Input": None, "Output": None, "Status": "Failed", "Message": str(e)}
        return make_response(jsonify(resp), 400)


@app.route('/api/decrypt', methods=['POST', 'GET'])
def decrypt():
    """
    This func will encrypt the given API
    :return: Payload and Status Code
    """
    try:
        key = load_key()
        data = request.json
        if data.get('Input') and len(data.get('Input')):
            enc_file = Fernet(key)
            decrypted_message = enc_file.decrypt(data.get('Input').encode('utf-8'))
            resp = {"input": data.get('Input'), "Output": decrypted_message.decode('utf-8'),
                    "Status": "success", "Message": "Decrypt success"}
            return make_response(jsonify(resp), 200)
        else:
            resp = {"Input": None, "Output": None, "Status": "Failed", "Message": "Empty Input"}
            return make_response(jsonify(resp), 200)
    except Exception as e:
        resp = {"input": None, "Output": None, "Status": "Failed", "Message": str(e)}
        return make_response(jsonify(resp), 400)


@app.errorhandler(404)
def page_not_found(err):
    _err = {
        "Input": request.json,
        "Output": "",
        "Status": "error",
        "Message": str(err)
    }
    return jsonify(_err)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
