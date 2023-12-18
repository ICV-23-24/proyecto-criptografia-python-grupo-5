from Cryptodome.Cipher import AES, DES3
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
from configparser import NoSectionError
from smb.SMBConnection import SMBConnection

server_name = 'samba'
server_ip = '127.0.0.1'
username = 'samba'
password = 'samba'


def conexion ():
        conec = SMBConnection(username, password, 'cliente', server_name, use_ntlm_v2=True)
        assert conec.connect(server_ip, 2900)
        return conec

# Trae los archivos de la carpeta del servidor
def listarclaveprivada(conec):
        listar1 = conec.listPath("claveprivada",'/')
        return listar1

def subirclaveprivada(conec,filename):
                # Aqui decimos donde va a cojer el archivo
                with open('uploads/'+filename,'rb') as data:
                        filename = '/' + filename
                        conec.storeFile("claveprivada",filename,data)
                return filename      

def descargarclaveprivada(conec,filename):
                # Aqui es donde se va descargar el archivo que recojes del servidor
                with open('uploads/'+filename,'wb') as des:
                        # Descargas el archivo indicado de la carpeta del servidor
                        conec.retrieveFile("claveprivada",filename,des)
                return filename

def listarficherosencriptados(conec):
        listar1 = conec.listPath("ficherosencriptados",'/')
        return listar1

def subirficherosencriptados(conec,filename):
                # Aqui decimos donde va a cojer el archivo
                with open('uploads/'+filename,'rb') as data:
                        file = '/' + filename
                        conec.storeFile("ficherosencriptados",filename,data)
                return filename      

def descargarficherosencriptados(conec,filename):
                # Aqui es donde se va descargar el archivo que recojes del servidor
                with open('uploads/'+filename,'wb') as des:
                        # Descargas el archivo indicado de la carpeta del servidor
                        conec.retrieveFile("ficherosencriptados",filename,des)
                return filename

def listarclavespublicas(conec):
        listar1 = conec.listPath("clavespublicas",'/')
        return listar1

def subirclavespublicas(conec,filename):
                # Aqui decimos donde va a cojer el archivo
                with open('uploads/'+filename,'rb') as data:
                        filename = '/' + filename
                        conec.storeFile("clavespublicas",filename,data)
                return filename      

def descargarclavespublicas(conec,filename):
                # Aqui es donde se va descargar el archivo que recojes del servidor
                with open('uploads/'+filename,'wb') as des:
                        # Descargas el archivo indicado de la carpeta del servidor
                        conec.retrieveFile("clavespublicas",filename,des)
                return filename

def listarficheros(conec):
        listar1 = conec.listPath("ficheros",'/')
        return listar1

def subirficheros(conec,filename):
                # Aqui decimos donde va a cojer el archivo
                with open('uploads/'+filename,'rb') as data:
                        file = '/' + filename
                        conec.storeFile("ficheros",filename,data)
                return filename      

def descargarficheros(conec,filename):
                # Aqui es donde se va descargar el archivo que recojes del servidor
                with open('uploads/'+filename,'wb') as des:
                        # Descargas el archivo indicado de la carpeta del servidor
                        conec.retrieveFile("ficheros",filename,des)
                return filename


# Encriptación AES
def encrypt_message_aes(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

# Desencriptación AES
def decrypt_message_aes(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

# Encriptación DES3
def encrypt_message_des3(message, key):
    key = key.encode('utf-8')
    cipher = DES3.new(pad(key, DES3.block_size), DES3.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), DES3.block_size))
    return b64encode(encrypted_message).decode('utf-8')

# Desencriptación DES3
def decrypt_message_des3(message, key):
    key = key.encode('utf-8')
    cipher = DES3.new(pad(key, DES3.block_size), DES3.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), DES3.block_size).decode('utf-8')
    return decrypted_message