from contextlib import _RedirectStream, redirect_stderr
from curses import flash
import os
from datetime import datetime
from flask import Flask, abort, render_template, request, send_file, url_for
import functions as f
# if platform.system() != 'Windows':
from curses import flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './UPLOAD/'
ALLOWED_EXTENSIONS = {'txt','gpg', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            #Guarda el archivo llamado encriptado.txt.gpg
            with open(UPLOAD_FOLDER+'encriptado.txt.gpg','w') as encry:
                #Pasa la escritura y lo mescla y se lo mete en el archivo encriptado.txt.gpg
                encry.write(encrypted_message)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
                 
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
             #Guarda el archivo llamado encriptado.txt.gpg
            with open(UPLOAD_FOLDER+'desencriptado.txt.gpg','rw') as decry:
                #Pasa la escritura y lo mescla y se lo mete en el archivo encriptado.txt.gpg
                decry.write(decrypted_message)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)
    return render_template("csimetrico.html")


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

@app.route("/PruebaSimetrica/")
def PruebaSimetrica():
    return render_template("PruebaSimetrica")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

