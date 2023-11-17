import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, send_from_directory
import functions as f
from werkzeug.utils import secure_filename
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#Mensaje a encriptar
message = b'Public and Private keys encryption'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route("/testingAsim", methods=['GET', 'POST'])
def testingAsim():
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == 'upload':
            file = request.files['file']
            # Revisa si no se ha seleccionado ningún archivo
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            # Guarda el archivo en caso de que sea válido
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))
        if mode == 'generate':
            #Generating private key (RsaKey object) of key length of 1024 bits
            private_key = RSA.generate(1024)
            #Generating the public key (RsaKey object) from the private key
            public_key = private_key.publickey()

            #Converting the RsaKey objects to string 
            private_pem = private_key.export_key().decode()
            public_pem = public_key.export_key().decode()

            #Writing down the private and public keys to 'pem' files
            with open('private_pem.pem', 'w') as pr:
                pr.write(private_pem)
            with open('public_pem.pem', 'w') as pu:
                pu.write(public_pem)

            return render_template('testingAsim.html',private_key=private_key,public_key=public_key,private_pem=private_pem,public_pem=public_pem,mode=mode)
        if mode == 'import':            #Importing keys from files, converting it into the RsaKey object   
            pr_key = RSA.import_key(open('private_pem.pem', 'r').read())
            pu_key = RSA.import_key(open('public_pem.pem', 'r').read())
            return render_template('testingAsim.html',pu_key=pu_key,pr_key=pr_key,mode=mode)

    # return render_template("csimetrico.html")


    return render_template("testingAsim.html")

@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/otro/")
def otro():
    return render_template("otro.html")



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/listar/")
def listar():
    return os.listdir(UPLOAD_FOLDER)

@app.route("/listar/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)