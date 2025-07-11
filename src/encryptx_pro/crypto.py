from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type
import os
import getpass

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LEN = 32  # AES-256

def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=6,
        memory_cost=262144,  # 256 MB
        parallelism=2,
        hash_len=KEY_LEN,
        type=Type.ID
    )

def encrypt_file(input_path, output_path, password=None):
    if password is None:
        password = getpass.getpass("Enter password: ")
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(output_path, 'wb') as f:
        f.write(salt + nonce + ciphertext)

def decrypt_file(input_path, output_path, password=None):
    if password is None:
        password = getpass.getpass("Enter password: ")

    with open(input_path, 'rb') as f:
        raw = f.read()

    salt = raw[:SALT_SIZE]
    nonce = raw[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
    ciphertext = raw[SALT_SIZE+NONCE_SIZE:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, 'wb') as f:
        f.write(plaintext)
