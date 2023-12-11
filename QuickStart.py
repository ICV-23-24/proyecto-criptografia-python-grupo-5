from configparser import NoSectionError
from smb.SMBConnection import SMBConnection

server_name = 'samba'
server_ip = '127.0.0.1'
username = 'samba'
password = 'samba'

descarga_archivos = './clavespublicas'

def conexion ():
        conec = SMBConnection(username, password, 'cliente', server_name, use_ntlm_v2=True)
        assert conec.connect(server_ip, 2900)
        return conec


def listarcarpetas1(conec):
        listar1 = conec.listPath("clavespublicas",'/')
        # for f in listar1:
        #     print (f.filename)
        return listar1

def listarcarpetas2(conec):
        listar2 = conec.listPath("ficherosencriptados",'/')
        for f in listar2:
            print(f.filename)

def subir1(conec,filename):
                with open('clavespublicas/'+filename,'rb') as data:
                        filename = '/' + filename
                        conec.storeFile("clavespublicas",filename,data)
                return filename      

def descargar1(conec,filename):
                with open('clavespublicas/'+filename,'wb') as des:
                        conec.retrieveFile("clavespublicas",filename,des)
                return filename





        






