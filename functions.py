from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode

def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

def decrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

# # Encriptado del archivo.

# def encrypt_file(file_path,key):
#     key = key.encode('utf-8')
#     # Lee el contenirdo del archivo para antes de encriptarlo
#     with open(file_path,'rb') as file:
#         original_data=file.read()
#     #Crea un objeto AES en modo ecb con la clave proporcionada y realiza el relleno del mensaje a encriptar
#     cipher = AES.new(pad(key.AES.block_size), AES.MODE_ECB)
#     # Esta parte encripta el mensaje del archivo y lo guarda en un formato base64.
#     encrypted_data = b64encode(cipher.encrypt(pad(original_data, AES.block_size))).decode('utf-8')
#     # Aqui se guardara el archivo una vez ya encriptado.
#     with open("archivo_encriptado.gpg",'w') as encrypted_file:
#         encrypted_file.write(encrypted_data)

# # Desencriptado del archivo.

# def decrypt_file(encrypted_file_path,key):
#     key = key.encode('utf-8')
#     # Lee el contenido del arcrhivo encriptado
#     with open(encrypted_file_path,'r') as file:
#         encrypted_data = file.read()
#     #Crea un objeto aes en modo ecb con la clave que proporcionamos y este procede a completar el mensaje.
#     cipher = AES.new(pad(key,AES.block_size),AES.MODE_ECB)
#     #Desencripta el mensaje del archivo y realiza el despad.
#     decrypted_data = unpad(cipher.decrypt(b64decode(encrypted_data)),AES.block_size)
#     #Guarda el archivo desencriptadoen un archivo (.txt)
#     with open("UPLOAD/archivo_descencriptado.txt",'wb') as decrypted_file:
#         decrypted_file.write(decrypted_data)
        