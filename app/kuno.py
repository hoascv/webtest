# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tempfile
import base64
import rsa
import OpenSSL.crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

import json

# from Crypto import Random


BLOCK_SIZE = 16

with tempfile.NamedTemporaryFile(suffix='.pem', delete=False) as t_pem:
    f_pem = open(t_pem.name, 'wb')
    pfx = open('./certificates/NVOTest.pfx', 'rb').read()
    p12 = OpenSSL.crypto.load_pkcs12(pfx, str.encode(''))
    f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
    ca = p12.get_ca_certificates()
    if ca is not None:
        for cert in ca:
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
    f_pem.close()

privkey = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey())

keyPriv = RSA.importKey(privkey)
modulusN = keyPriv.n
pubExpE = keyPriv.e
priExpD = keyPriv.d
primeP = keyPriv.p
primeQ = keyPriv.q

private_key = RSA.construct((modulusN, pubExpE, priExpD, primeP, primeQ))

pubkey = private_key.publickey().exportKey('PEM')

#key = b'Sixteen byte key'
key = "HSKEY00000000000".encode("utf-8")
iv = b'Sixteen byte key'
print("Key:")
print(key)
print("IV:")
print(iv)

pubkey = rsa.key.PublicKey.load_pkcs1_openssl_pem(pubkey.decode('utf-8'))
print("Public Key: ")
print(pubkey)
private_key = rsa.PrivateKey.load_pkcs1(
    OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, p12.get_privatekey()), format='DER')
print("Private Key: ")
print(private_key)

encryptRSAkey = rsa.encrypt(key, pubkey)
encryptRSAiv = rsa.encrypt(iv, pubkey)

print(encryptRSAkey)

encryptedKey = base64.b64encode(encryptRSAkey)
encryptedIV = base64.b64encode(encryptRSAiv)

print("Encrypted Key: ")
print(encryptedKey)
print("Encrypted IV: ")
print(encryptedIV)

cipher = AES.new(key, AES.MODE_CBC, iv)

F = open("./features_test_data/183da23022e4_20150507-083000.csv", "r")
fileData = F.read()
print(fileData)
msgBytePad = bytes(fileData, 'utf-8')
length = 16 - (len(msgBytePad) % 16)
msgBytePad += bytes([length]) * length

msg = cipher.encrypt(msgBytePad)
msgb64 = base64.b64encode(msg)
print("Encoded message: ")
print(msgb64)

signature = rsa.sign(msg, private_key, 'SHA-256')
encode = base64.b64encode(signature)
print("Encoded Signature: ")
print(encode)

print('tamanho: {}'.format(len(msgb64)))