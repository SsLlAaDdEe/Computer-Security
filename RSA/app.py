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

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    for _ in range(k):
        a = random.randint(2, n - 1)
        if gcd(n, a) != 1:
            return False
        if pow(a, n - 1, n) != 1:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    key, n = public_key
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    key, n = private_key
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files or 'p' not in request.form or 'q' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    p = request.form['p']
    q = request.form['q']

    if file.filename == '' or not p.isdigit() or not q.isdigit():
        return redirect(request.url)

    p = int(p)
    q = int(q)
    
    public, private = generate_keypair(p, q)
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'cipherText.txt')
    
    file.save(input_filepath)
    
    with open(input_filepath, 'r') as infile:
        plaintext = infile.read()
    
    encrypted_message = encrypt(public, plaintext)
    
    with open(output_filepath, 'w') as outfile:
        outfile.write(' '.join(map(str, encrypted_message)))
    
    return send_file(output_filepath, as_attachment=True, download_name='cipherText.txt')

if __name__ == '__main__':
    app.run(debug=True)
