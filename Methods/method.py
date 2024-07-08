from DB import db
from Models import UserModel
import uuid
from cryptography.fernet import Fernet

class Methods():
    #Global variables declared
    conn = db.Mysqlconfig.conn
    cur = db.Mysqlconfig.cursor
    err =db.Mysqlconfig.error
    #--------
    # Generate a key for encryption (keep this key safe)
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    def updatesession(id):
         tuuid=uuid1()
         sql_query=f"CALL update_sessionid_sp({id},{tuuid})"
         cur.execute(sql_query)
         result=cur.fetchone()
         return ''

 
    #encryption method
    def encryption(data):
        try:
            encrypted_data = cipher_suite.encrypt(data.encode())
            return encrypted_data
            
        except Exception as error:
            return ''

    # decryption method
    def decryption(encrypted_data):
        try:
             decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
             return decrypted_data 
             
        except Exception as error:
            return ""

         