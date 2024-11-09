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

def caesar(plainText, shift): 
    cipherText = ""
    for char in plainText:
        if char.isalpha():
            stayInAlphabet = ord(char) + shift 
            if char.islower():
                if stayInAlphabet > ord('z'):
                    stayInAlphabet -= 26
                elif stayInAlphabet < ord('a'):
                    stayInAlphabet += 26
            elif char.isupper():
                if stayInAlphabet > ord('Z'):
                    stayInAlphabet -= 26
                elif stayInAlphabet < ord('A'):
                    stayInAlphabet += 26
            finalLetter = chr(stayInAlphabet)
            cipherText += finalLetter
        else:
            cipherText += char  # Keep non-alphabetic characters unchanged
    return cipherText

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files or 'shift' not in request.form:
        return redirect(request.url)
    
    file = request.files['file']
    shift = request.form['shift']
    
    if file.filename == '' or not shift.isdigit():
        return redirect(request.url)
    
    shift = int(shift)
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'ciphertext.txt')
    
    file.save(input_filepath)
    
    with open(input_filepath, 'r') as infile:
        plainText = infile.read()
    
    cipherText = caesar(plainText, shift)
    
    with open(output_filepath, 'w') as outfile:
        outfile.write(cipherText)
    
    return send_file(output_filepath, as_attachment=True, download_name='ciphertext.txt')

if __name__ == '__main__':
    app.run(debug=True)
