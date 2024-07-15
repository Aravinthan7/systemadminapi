from DB import db
from Models import UserModel
import uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

class Methods():
    #Global variables declared
    conn = db.Mysqlconfig.conn
    cur = db.Mysqlconfig.cursor
    err =db.Mysqlconfig.error
    #--------
    # Generate a key for encryption (keep this key safe)
    # Example usage to generate a valid AES key
    secret_key = "my_secret_key_123"
    valid_aes_key = generate_key(secret_key)

    def updatesession(id):
         tuuid=uuid1()
         sql_query=f"CALL update_sessionid_sp({id},{tuuid})"
         cur.execute(sql_query)
         result=cur.fetchone()
         return result

 
    #encryption method
    def generate_key(secret_key):

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(secret_key.encode('utf-8'))
        return digest.finalize()[:32]  # Limit key size to 32 bytes (AES-256)



    # decryption method
    def decryption(encrypted_data):
        try:
             decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
             return decrypted_data 
             
        except Exception as error:
            return ""

         