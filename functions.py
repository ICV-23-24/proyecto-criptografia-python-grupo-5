from Cryptodome.Cipher import AES, DES3
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode

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