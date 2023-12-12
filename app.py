from datetime import datetime
from flask import Flask, render_template, request
import functions as f
# Importar la funciones de conexion,listarcarpetas,subir y descargar del quickstart.py
from QuickStart import conexion,listarcarpetas1,subir1,descargar1

app = Flask(__name__)


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

@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/otro/", methods=['GET', 'POST'])
def otro():
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == 'listar':
            # Aqui llamamos a la funcion de conexion y la de  listarcarpetas
            conec = conexion()
            carpetas = listarcarpetas1(conec)
            return render_template('otro.html', carpetas=carpetas,mode=mode)
        if mode == 'subir':
            conec = conexion()
            # recoges el archivo
            file=request.files['file']
            # recoges el nombre del archivo
            filename = file.filename
            # aqui llamas a la funcion de subir el archivo
            subir = subir1(conec,filename=filename)
            return render_template('otro.html', subir=subir,mode=mode)
        if mode == 'descargar':
            conec = conexion()
            # recoges el archivo
            filename = request.form['filename']
            # aqui llamas a la funcion de descargar el archivo
            descargar = descargar1(conec,filename=filename)
            return render_template('otro.html', descargar=descargar,mode=mode)
    return render_template('otro.html')

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