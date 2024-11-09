from flask import Flask, request, render_template, redirect, url_for, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def vigenere_otp_encrypt(message, key):
    encrypted_message = ""
    for i in range(len(message)):
        encrypted_char = chr((ord(message[i]) + ord(key[i])) % 256)
        encrypted_message += encrypted_char
    return encrypted_message

def vigenere_otp_decrypt(encrypted_message, key):
    decrypted_message = ""
    for i in range(len(encrypted_message)):
        decrypted_char = chr((ord(encrypted_message[i]) - ord(key[i])) % 256)
        decrypted_message += decrypted_char
    return decrypted_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files or 'keyfile' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    keyfile = request.files['keyfile']

    if file.filename == '' or keyfile.filename == '':
        return redirect(request.url)

    message = file.read().decode('utf-8')
    key = keyfile.read().decode('utf-8')

    if len(key) < len(message):
        return "Error: Key length must be equal to or greater than the message length."

    encrypted_message = vigenere_otp_encrypt(message, key)

    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'cipherText.txt')
    with open(output_filepath, 'w') as outfile:
        outfile.write(encrypted_message)

    return send_file(output_filepath, as_attachment=True, download_name='cipherText.txt')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files or 'keyfile' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    keyfile = request.files['keyfile']

    if file.filename == '' or keyfile.filename == '':
        return redirect(request.url)

    encrypted_message = file.read().decode('utf-8')
    key = keyfile.read().decode('utf-8')

    decrypted_message = vigenere_otp_decrypt(encrypted_message, key)

    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'plainText.txt')
    with open(output_filepath, 'w') as outfile:
        outfile.write(decrypted_message)

    return send_file(output_filepath, as_attachment=True, download_name='plainText.txt')

if __name__ == '__main__':
    app.run(debug=True)
