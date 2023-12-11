import fnmatch
import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, send_file, send_from_directory
import functions as f
from werkzeug.utils import secure_filename
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

# Directorio de almacenamiento de claves
UPLOAD_FOLDER = './uploads/'
# Extensiones permitidas para la subida de archivos
ALLOWED_EXTENSIONS = {'pem'}

# Listado de archivos del directorio de almacenamiento de claves
list_file = os.listdir(UPLOAD_FOLDER)
list_publickey = fnmatch.filter(list_file, '*_public.pem')
list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
list_button = list_publickey

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Comprobación de validez de subida de archivo
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Reemplaza la ruta raiz
@app.route("/")
def home():
    return render_template("home.html")

# Cifrado simétrico
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == 'encrypt_aes':
            key = request.form['key']
            message = request.form['message']
            key_name = request.form['key_name']
            message_name = request.form['message_name']
            # Asigna un nombre al archivo con la clave simétrica
            keyfile_name = key_name+'_key.txt.gpg'
            # Asigna un nombre al archivo con el mensaje encriptado
            messagefile_name = message_name+'_mensaje.txt.gpg'
            # Utiliza la función de encriptacion AES para encriptar el mensaje con la clave
            encrypted_message = f.encrypt_message_aes(message, key)

            # Guarda el mensaje encriptado en un archivo
            with open(UPLOAD_FOLDER+messagefile_name, 'w') as encrypted:
                encrypted.write(encrypted_message)
            # Guarda la clave en un archivo
            with open(UPLOAD_FOLDER+keyfile_name, 'w') as key_encrypted:
                key_encrypted.write(key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
            return render_template('csimetrico.html', encrypted_message=encrypted_message,list_encryptedfile=list_encryptedfile,mode=mode)
        if mode == 'encrypt_des3':
            key = request.form['key']
            message = request.form['message']
            key_name = request.form['key_name']
            message_name = request.form['message_name']
            # Asigna un nombre al archivo con la clave simétrica
            keyfile_name = key_name+'_key.txt.gpg'
            # Asigna un nombre al archivo con el mensaje encriptado
            messagefile_name = message_name+'_mensaje.txt.gpg'
            # Utiliza la función de encriptacion DES3 para encriptar el mensaje con la clave
            encrypted_message = f.encrypt_message_des3(message, key)

            # Guarda el mensaje encriptado en un archivo
            with open(UPLOAD_FOLDER+messagefile_name, 'w') as encrypted:
                encrypted.write(encrypted_message)

            # Guarda la clave en un archivo
            with open(UPLOAD_FOLDER+keyfile_name, 'w') as key_encrypted:
                key_encrypted.write(key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
            return render_template('csimetrico.html', encrypted_message=encrypted_message,list_encryptedfile=list_encryptedfile,mode=mode)        
        if mode == 'decrypt_aes':
            selection = request.form['selection']
            key_select = request.form['key_select']
            # Abre el archivo con el mensaje seleccionado y lee el contenido
            with open(UPLOAD_FOLDER+selection, 'r') as gpg_message_file:
                gpg_message = gpg_message_file.read()
            # Abre el archivo con la clave seleccionado y lee el contenido
            with open(UPLOAD_FOLDER+key_select, 'r') as gpg_key_file:
                gpg_key = gpg_key_file.read()
            # Utiliza la función de desencriptado AES para descifrar el mensaje seleccionado con la clave seleccionada
            decrypted_message = f.decrypt_message_aes(gpg_message,gpg_key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
            return render_template('csimetrico.html', decrypted_message=decrypted_message,list_encryptedfile=list_encryptedfile,mode=mode)
        if mode == 'decrypt_des3':
            selection = request.form['selection']
            key_select = request.form['key_select']
            # Abre el archivo con el mensaje seleccionado y lee el contenido
            with open(UPLOAD_FOLDER+selection, 'r') as gpg_message_file:
                gpg_message = gpg_message_file.read()
            # Abre el archivo con la clave seleccionado y lee el contenido
            with open(UPLOAD_FOLDER+key_select, 'r') as gpg_key_file:
                gpg_key = gpg_key_file.read()
            # Utiliza la función de desencriptado DES3 para descifrar el mensaje seleccionado con la clave seleccionada
            decrypted_message = f.decrypt_message_des3(gpg_message,gpg_key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
            return render_template('csimetrico.html', decrypted_message=decrypted_message,list_encryptedfile=list_encryptedfile,mode=mode)
        
    list_file = os.listdir(UPLOAD_FOLDER)
    list_encryptedfile = fnmatch.filter(list_file, '*.gpg')
    return render_template("csimetrico.html",list_encryptedfile=list_encryptedfile)

# Cifrado Asimétrico
@app.route("/casimetrico", methods=['GET', 'POST'])
def casimetrico():
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
        if mode == 'list':
            return render_template('casimetrico.html',list_button=list_button,list_publickey=list_publickey,mode=mode)
        if mode == 'generate':
            pem_name = request.form['pem_name']
            # Genera clave privada con algoritmo RSA con tamaño de 1024 bits
            private_key = RSA.generate(1024)
            # Genera la clave pública(RsaKey) desde la clave privadas
            public_key = private_key.publickey()
            # Convierte los RsaKey a string
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            # Guarda las claves pública y privada en archivos .pem
            public_pem_name = pem_name+'_public.pem'
            private_pem_name = pem_name+'_private.pem'
            
            with open(UPLOAD_FOLDER+private_pem_name, 'w') as pr:
                pr.write(private_pem)
            with open(UPLOAD_FOLDER+public_pem_name, 'w') as pu:
                pu.write(public_pem)
            return render_template('casimetrico.html',private_key=private_key,list_publickey=list_publickey,mode=mode)
        if mode == 'encrypt':
            selection = request.form['selection']
            # Obtiene el nombre asociado a los archivos de claves
            global name_only
            name_only = selection.split('_')[0]
            with open(UPLOAD_FOLDER+selection, 'r') as pu_pem:
                pu_key_pem = pu_pem.read()
                pu_key = RSA.importKey(pu_key_pem)
            message = request.form['message']
            message = bytes(message,'utf-8')
            # Utiliza el protocolo de encriptación PKCS1_OAEP para cifrar con la clave pública
            cipher = PKCS1_OAEP.new(pu_key)
            global cipher_text
            # Encripta el mensaje
            cipher_text = cipher.encrypt(message)
            # Codifica el mensaje en B64
            cipher_text_b64 = base64.b64encode(cipher_text).decode('utf-8')
            return render_template('casimetrico.html',cipher_text_b64=cipher_text_b64,name_only=name_only,list_publickey=list_publickey,mode=mode)
        if mode == 'decrypt':
            # Recibe el nombre asociado a los archivos de claves
            associated_private_key_name = name_only+'_private.pem'
            # Importa la clave privada
            with open(UPLOAD_FOLDER+associated_private_key_name, 'r') as pr_pem:
                pr_key_pem = pr_pem.read()
                pr_key = RSA.importKey(pr_key_pem)
            encrypted_message_b64 = request.form['encrypted_message']
            # Convierte el mensaje de B64 a bytes
            encrypted_message = base64.b64decode(encrypted_message_b64)
            # Utiliza el protocolo de encriptación PKCS1_OAEP para descifrar con la clave privada
            decipher = PKCS1_OAEP.new(pr_key)
            # Descifra el mensaje
            decipher_text = decipher.decrypt(encrypted_message)
            return render_template('casimetrico.html',decipher_text=decipher_text,list_publickey=list_publickey,mode=mode)
    return render_template("casimetrico.html",list_publickey=list_publickey)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

# Ruta de descarga de archivos
@app.route('/uploads/<path:file>', methods=['GET', 'POST'])
def download(file):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_file(uploads+file)