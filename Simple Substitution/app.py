from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

alphabet = 'abcdefghijklmnopqrstuvwxyz.,! '
key = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'

def makeKey(alphabet):
    alphabet = list(alphabet)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def encrypt(plaintext, key, alphabet):
    keyMap = dict(zip(alphabet, key))
    return ''.join(keyMap.get(c.lower(), c) for c in plaintext)

def decrypt(cipher, key, alphabet):
    keyMap = dict(zip(key, alphabet))
    return ''.join(keyMap.get(c.lower(), c) for c in cipher)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'cipherText.txt')
    
    file.save(input_filepath)
    
    with open(input_filepath, 'r') as infile:
        plaintext = infile.read()
    
    encrypted_text = encrypt(plaintext, key, alphabet)
    
    with open(output_filepath, 'w') as outfile:
        outfile.write(encrypted_text)
    
    return send_file(output_filepath, as_attachment=True, download_name='cipherText.txt')

if __name__ == '__main__':
    app.run(debug=True)


