from Crypto.PublicKey import RSA
import rsa
import tempfile
import OpenSSL
from Crypto.Signature import PKCS1_v1_5
import base64
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5


class RSAHelper(object):
    #def __init__(self, server_certificate, client_key):
    #    self.server_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
    #                                                             open(server_certificate).read())
    #    self.pubKey = self.server_certificate.get_pubkey()
    #    with open(client_key, 'r') as key:
    #        self.privateKey = RSA.importKey(key.read(), passphrase='')
    def __init__(self, pfx_certificate, pfx_password, server_certificate_path, client_key_path):
        server_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                                             open(server_certificate_path).read())

        cert_der = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, server_certificate)
        self.recipient_public_key = RSA.import_key(cert_der)

        with open(client_key_path) as private_key:  # testing not working for private key from pem format
            self.temp_client_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, private_key.read(), str.encode(pfx_password))
            self.client_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, self.temp_client_key)
            #print(base64.b64encode(self.client_key))

        with tempfile.NamedTemporaryFile(suffix='.pem', delete=False) as t_pem:  #pfx format
            f_pem = open(t_pem.name, 'wb')
            pfx = open(pfx_certificate, 'rb').read()
            p12 = OpenSSL.crypto.load_pkcs12(pfx, str.encode(pfx_password))
            f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
            ca = p12.get_ca_certificates()
            if ca is not None:
                for cert in ca:
                    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
            f_pem.close()

        temp_private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey())

        keyPriv = RSA.importKey(temp_private_key)
        modulusN = keyPriv.n
        pubExpE = keyPriv.e
        priExpD = keyPriv.d
        primeP = keyPriv.p
        primeQ = keyPriv.q

        self.private_key = RSA.construct((modulusN, pubExpE, priExpD, primeP, primeQ))

       # self.private_key = rsa.PrivateKey.load_pkcs1(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, p12.get_privatekey()), format='DER')

    def encrypt_info_key(self, key):
        return rsa.encrypt(key, self.recipient_public_key)

    def encrypt_info_iv(self, iv):
        return rsa.encrypt(iv, self.recipient_public_key)

    def signatures(self, message):

        signer = PKCS1_v1_5.new(self.private_key)
        digest = SHA.new()
        digest.update(message)
        return signer.sign(digest)
        #return rsa.sign(message, self.private_key, 'SHA-1')