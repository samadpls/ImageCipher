from flask import Flask, request, send_file, jsonify
from image_cipher import ImageCipher
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
cipher = ImageCipher()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/encode', methods=['POST'])
def encode_image():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({'error': 'No image or message provided'}), 400

    image = request.files['image']
    message = request.form['message']
    encrypt = request.form.get('encrypt', 'true').lower() == 'true'

    image_path = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))
    image.save(image_path)

    encoded_image_path = cipher.encode(image_path, message, encrypt)
    return send_file(encoded_image_path, as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    key = request.form.get('key', None)

    image_path = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))
    image.save(image_path)

    message = cipher.decode(image_path, key)
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
