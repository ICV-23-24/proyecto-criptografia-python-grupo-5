from datetime import datetime
from flask import Flask, render_template, request
import functions as f
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
        # file=request.files['file']

        if mode == 'listar':
            conec = conexion()
            carpetas = listarcarpetas1(conec)
            return render_template('otro.html', carpetas=carpetas,mode=mode)
        if mode == 'subir':
            conec = conexion()
            file=request.files['file']
            filename = file.filename
            subir = subir1(conec,filename=filename)
            return render_template('otro.html', subir=subir,mode=mode)
        if mode == 'descargar':
            conec = conexion()
            filename = request.form['filename']
            # file=request.files['file']
            # filename = file.filename
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