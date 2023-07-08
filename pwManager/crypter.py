import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#generate a unique key for each user using their hashed master password and salt
def generate_key(hashed_pw, salt):
    hashed_bytes = hashed_pw.encode("utf-8")
    salted_bytes = salt.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salted_bytes,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(hashed_bytes))
    return key

#encrypts a account's password, used for password creation
def encrypt(key, password):
    crypter = Fernet(key)
    encrypted_password = crypter.encrypt(password.encode())
    return encrypted_password.decode("utf-8")

#decrypts a account's password, used for password retrieval
def decrypt(key, encrypted_password):
    crypter = Fernet(key)
    password = crypter.decrypt(encrypted_password)
    return password.decode("utf-8")