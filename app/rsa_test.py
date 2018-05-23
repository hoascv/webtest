from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import OpenSSL
from Crypto.PublicKey import RSA
import rsa

data = "abc".encode("utf-8")

#print (open("pubkey.der").read())
server_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                                                     open('./certificates/NVOTest.pfx.cer.pem').read())
cert_der = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, server_certificate)
recipient_key = RSA.import_key(cert_der)
session_key = get_random_bytes(16)
#cipher_aes = AES.new(session_key, AES.MODE_CBCX)
#cipher_rsa = PKCS1_OAEP.new(recipient_key)
rsa.encrypt(data, recipient_key)