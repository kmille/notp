import os
import os.path
import sys
import binascii
import getpass

import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import cryptography.exceptions 

base_dir = "data"

def a(s):
    return binascii.hexlify(s).decode()


def b(s):
    return binascii.unhexlify(s)


def test_encryption():
    data = b"a secrsddsfdsfdsffdset message"
    nonce = b"84b41aa0e4c1277ee3d785e2"
    key = hashlib.sha256(getpass.getpass().encode()).digest()
    print("data: '{}'  nonce: {}   key: {}".format(data.decode(), a(nonce), a(key)))

    # encrypt
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, data, None)
    print("Ciphertext: {}".format(a(ct)))

    # decrypt
    msg = aesgcm.decrypt(nonce, ct, None)
    print("Plaintext: {}".format(msg.decode()))


def encrypt_token(context):
    token_file = os.path.join(base_dir, context)
    nonce = os.urandom(16)
    data = input("OTP Token: ")
    key = hashlib.sha256(getpass.getpass().encode()).digest()
    print("data: '{}'  nonce: {}   key: {}".format(data, a(nonce), a(key)))

    # encrypt
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, data.encode(), None)
    print("Ciphertext: {}".format(a(ct)))

    with open(token_file, "w") as f:
        f.write(a(nonce) + "\n" + a(ct))
    print("Wrote encrpyted OTP Token to file")


def decrypt_token(context):
    token_file = os.path.join(base_dir, context)
    with open(token_file, "r") as f:
        f = f.read()
    nonce, ciphertext = f.splitlines()
    #print(nonce, ciphertext)
    key = hashlib.sha256(getpass.getpass().encode()).digest()
    aesgcm = AESGCM(key)
    try:
        token = aesgcm.decrypt(b(nonce), b(ciphertext), None).decode()
        print("Decrypted: {}".format(token))
    except cryptography.exceptions.InvalidTag:
        print("wrong password")
        return None
    return token


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("encrypt or decrypt <context>")
        exit()
    if sys.argv[1]  == "encrypt":
        encrypt_token(sys.argv[2])
    if sys.argv[1]  == "decrypt":
        decrypt_token(sys.argv[2])
