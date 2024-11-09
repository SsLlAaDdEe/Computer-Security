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

def vigenere_encrypt(plain_text, key):
    key = key.upper()
    cipher_text = ''
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            if char.islower():
                cipher_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                cipher_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            key_index += 1
        else:
            cipher_char = char
        cipher_text += cipher_char
    return cipher_text

def vigenere_decrypt(cipher_text, key):
    key = key.upper()
    plain_text = ''
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            if char.islower():
                plain_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            else:
                plain_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            key_index += 1
        else:
            plain_char = char
        plain_text += plain_char
    return plain_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files or 'key' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    key = request.form['key']

    if file.filename == '' or key == '':
        return redirect(request.url)

    plain_text = file.read().decode('utf-8')

    cipher_text = vigenere_encrypt(plain_text, key)

    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'cipherText.txt')
    with open(output_filepath, 'w') as outfile:
        outfile.write(cipher_text)

    return send_file(output_filepath, as_attachment=True, download_name='cipherText.txt')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files or 'key' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    key = request.form['key']

    if file.filename == '' or key == '':
        return redirect(request.url)

    cipher_text = file.read().decode('utf-8')

    plain_text = vigenere_decrypt(cipher_text, key)

    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'plainText.txt')
    with open(output_filepath, 'w') as outfile:
        outfile.write(plain_text)

    return send_file(output_filepath, as_attachment=True, download_name='plainText.txt')

if __name__ == '__main__':
    app.run(debug=True)
