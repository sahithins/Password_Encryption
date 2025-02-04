from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

master_password = b"?Master@13119#"
salt = b"salt@@@salt" 

admin_username = "admin"

# Function to generate a secure key from a master password using PBKDF2
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key

# Function to encrypt data using AES
def encrypt_data(data, key):
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()  # Pad the data to be encrypted
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

# Function to decrypt data using AES
def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]  # Extract the initialization vector
    ciphertext = encrypted_data[16:]  # Extract the ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()  # Unpad the decrypted data
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

if __name__ == "__main__":
    # Example usage
    master_password = b"?Master@13119#"
    salt = os.urandom(16)  # Generate a random salt
    key = generate_key(master_password, salt)

    # Data to encrypt
    data_to_encrypt = b"Sensitive information"

    # Encrypt the data
    encrypted_data = encrypt_data(data_to_encrypt, key)

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, key)

    print("Original data:", data_to_encrypt)
    print("Encrypted data:", encrypted_data)
    print("Decrypted data:", decrypted_data)
