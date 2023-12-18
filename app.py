import fnmatch
import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, send_file, send_from_directory
import functions as f
from werkzeug.utils import secure_filename
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
from functions import conexion,listarclaveprivada,subirclaveprivada,descargarclaveprivada,listarficherosencriptados,subirficherosencriptados,descargarficherosencriptados,listarclavespublicas,subirclavespublicas,descargarclavespublicas,listarficheros,subirficheros,descargarficheros

# Directorio de almacenamiento de claves
UPLOAD_FOLDER = './uploads/'
# Extensiones permitidas para la subida de archivos
symmetric_extension = {'gpg'}
asymmetric_extension = {'pem'}

# Listado de archivos del directorio de almacenamiento de claves
list_file = os.listdir(UPLOAD_FOLDER)
list_publickey = fnmatch.filter(list_file, '*_public.pem')
list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
list_button_publickey = list_publickey
list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
list_button_key = list_symmetric_key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Comprobación de validez de subida de archivo de cifrado asimétrico
def allowed_file_asymmetric(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in asymmetric_extension

# Comprobación de validez de subida de archivo simétrico
def allowed_file_symmetric(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in symmetric_extension

# Reemplaza la ruta raiz
@app.route("/")
def home():
    return render_template("home.html")

# Cifrado simétrico
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == 'upload':
            file = request.files['file']
            # Revisa si no se ha seleccionado ningún archivo
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            # Guarda el archivo en caso de que sea válido
            if file and allowed_file_symmetric(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))
        if mode == 'subirprivada':
            conec = conexion()
            # recoges el archivo
            file=request.files['file']
            # recoges el nombre del archivo
            filename = file.filename
            # aqui llamas a la funcion de subir el archivo
            subirprivada = subirclaveprivada(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html',list_symmetric_key_samba=list_symmetric_key_samba,list_button_key=list_button_key,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,subirprivada=subirprivada,mode=mode)
        if mode == 'subirencriptado':
            conec = conexion()
            # recoges el archivo
            file=request.files['file']
            # recoges el nombre del archivo
            filename = file.filename
            # aqui llamas a la funcion de subir el archivo
            subirencriptado = subirficherosencriptados(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html',list_symmetric_key_samba=list_symmetric_key_samba,list_button_key=list_button_key,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,subirencriptado=subirencriptado,mode=mode)
        if mode == 'list_symmetric_keys':
            conec = conexion()
            list_symmetric_key_samba = listarclaveprivada(conec)
            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            list_button_key = list_symmetric_key
            return render_template('csimetrico.html',list_symmetric_key_samba=list_symmetric_key_samba,list_button_key=list_button_key,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)
        if mode == 'list_symmetric_messages':
            conec = conexion()
            list_symmetric_message_samba = listarficherosencriptados(conec)
            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            list_button_message = list_symmetric_message

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html',list_symmetric_message_samba=list_symmetric_message_samba,list_button_message=list_button_message,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)
        if mode == 'descargarprivada':
            conec = conexion()
            # recoges el archivo
            filename = request.form['filename']
            # aqui llamas a la funcion de descargar el archivo
            descargarprivada = descargarclaveprivada(conec,filename=filename)
            return render_template('csimetrico.html',list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,descargarprivada=descargarprivada,mode=mode)
        if mode == 'descargarencriptados':
            conec = conexion()
            # recoges el archivo
            filename = request.form['filename']
            # aqui llamas a la funcion de descargar el archivo
            descargarencriptados = descargarficherosencriptados(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html',list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,descargarencriptados=descargarencriptados,mode=mode)
        if mode == 'encrypt_aes':
            key = request.form['key']
            message = request.form['message']
            key_name = request.form['key_name']
            message_name = request.form['message_name']
            # Asigna un nombre al archivo con la clave simétrica
            keyfile_name = key_name+'_key.txt.gpg'
            # Asigna un nombre al archivo con el mensaje encriptado
            messagefile_name = message_name+'_symmetricmessage.txt.gpg'
            # Utiliza la función de encriptacion AES para encriptar el mensaje con la clave
            encrypted_message = f.encrypt_message_aes(message, key)

            # Guarda el mensaje encriptado en un archivo
            with open(UPLOAD_FOLDER+messagefile_name, 'w') as encrypted:
                encrypted.write(encrypted_message)
            # Guarda la clave en un archivo
            with open(UPLOAD_FOLDER+keyfile_name, 'w') as key_encrypted:
                key_encrypted.write(key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html',encrypted_message=encrypted_message,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)
        if mode == 'encrypt_des3':
            key = request.form['key']
            message = request.form['message']
            key_name = request.form['key_name']
            message_name = request.form['message_name']
            # Asigna un nombre al archivo con la clave simétrica
            keyfile_name = key_name+'_key.txt.gpg'
            # Asigna un nombre al archivo con el mensaje encriptado
            messagefile_name = message_name+'_symmetricmessage.txt.gpg'
            # Utiliza la función de encriptacion DES3 para encriptar el mensaje con la clave
            encrypted_message = f.encrypt_message_des3(message, key)

            # Guarda el mensaje encriptado en un archivo
            with open(UPLOAD_FOLDER+messagefile_name, 'w') as encrypted:
                encrypted.write(encrypted_message)

            # Guarda la clave en un archivo
            with open(UPLOAD_FOLDER+keyfile_name, 'w') as key_encrypted:
                key_encrypted.write(key)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html', encrypted_message=encrypted_message,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)        
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
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html', decrypted_message=decrypted_message,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)
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
            list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
            list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
            return render_template('csimetrico.html', decrypted_message=decrypted_message,list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message,mode=mode)
        
    list_file = os.listdir(UPLOAD_FOLDER)
    list_symmetric_key = fnmatch.filter(list_file, '*_key.txt.gpg')
    list_symmetric_message = fnmatch.filter(list_file, '*_symmetricmessage.txt.gpg')
    return render_template("csimetrico.html",list_symmetric_key=list_symmetric_key,list_symmetric_message=list_symmetric_message)

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
            if file and allowed_file_asymmetric(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))
        if mode == 'list_asymmetric_keys':
            conec = conexion()
            list_publickey_samba = listarclavespublicas(conec)
            list_file = os.listdir(UPLOAD_FOLDER)
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_button_key = list_publickey
            return render_template('casimetrico.html',list_publickey_samba=list_publickey_samba,list_button_key=list_button_key,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'list_asymmetric_messages':
            conec = conexion()
            list_asymmetric_message_samba = listarficheros(conec)
            list_file = os.listdir(UPLOAD_FOLDER)
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_button_message = list_asymmetric_message
            return render_template('casimetrico.html',list_asymmetric_message_samba=list_asymmetric_message_samba,list_button_message=list_button_message,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'descargarpublica':
            conec = conexion()
            # recoges el archivo
            filename = request.form['filename']
            # aqui llamas a la funcion de descargar el archivo
            descargarpublica = descargarclavespublicas(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html',descargarpublica=descargarpublica,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'descargarfichero':
            conec = conexion()
            # recoges el archivo
            filename = request.form['filename']
            # aqui llamas a la funcion de descargar el archivo
            descargarfichero = descargarficheros(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html', descargarfichero=descargarfichero,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'subirpublica':
            conec = conexion()
            # recoges el archivo
            file=request.files['file']
            # recoges el nombre del archivo
            filename = file.filename
            # aqui llamas a la funcion de subir el archivo
            subirpublica = subirclavespublicas(conec,filename=filename)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html', subirpublica=subirpublica,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'subirfichero':
            conec = conexion()
            # recoges el archivo
            file=request.files['file']
            # recoges el nombre del archivo
            filename = file.filename
            # aqui llamas a la funcion de subir el archivo
            subirfichero = subirficheros(conec,filename=filename)
            return render_template('casimetrico.html', subirfichero=subirfichero,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
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

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html',private_key=private_key,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'encrypt':
            selection = request.form['selection']
            message_name = request.form['message_name']
            asymmetric_message_name = message_name+'_asymmetricmessage.txt.gpg'
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

            with open(UPLOAD_FOLDER+asymmetric_message_name, 'w') as message_encrypted:
                message_encrypted.write(cipher_text_b64)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html',name_only=name_only,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)
        if mode == 'decrypt':
            # Recibe el nombre asociado a los archivos de claves
            associated_private_key_name = name_only+'_private.pem'
            # Importa la clave privada
            with open(UPLOAD_FOLDER+associated_private_key_name, 'r') as pr_pem:
                pr_key_pem = pr_pem.read()
                pr_key = RSA.importKey(pr_key_pem)
            selection_encrypted_message= request.form['selection_encrypted_message']
            with open(UPLOAD_FOLDER+selection_encrypted_message, 'r') as encrypted_message:
                encrypted_message_b64 = encrypted_message.read()
            # Convierte el mensaje de B64 a bytes
            encrypted_message = base64.b64decode(encrypted_message_b64)
            # Utiliza el protocolo de encriptación PKCS1_OAEP para descifrar con la clave privada
            decipher = PKCS1_OAEP.new(pr_key)
            # Descifra el mensaje
            decipher_text = decipher.decrypt(encrypted_message)

            list_file = os.listdir(UPLOAD_FOLDER)
            list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
            list_publickey = fnmatch.filter(list_file, '*_public.pem')
            return render_template('casimetrico.html',decipher_text=decipher_text,list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message,mode=mode)

    list_file = os.listdir(UPLOAD_FOLDER)    
    list_asymmetric_message = fnmatch.filter(list_file, '*_asymmetricmessage.txt.gpg')
    list_publickey = fnmatch.filter(list_file, '*_public.pem')
    return render_template("casimetrico.html",list_publickey=list_publickey,list_asymmetric_message=list_asymmetric_message)

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

# Ruta de descarga de archivos
@app.route('/uploads/<path:file>', methods=['GET', 'POST'])
def download(file):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_file(uploads+file)