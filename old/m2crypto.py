#import M2Crypto

#cert = M2Crypto.X509.load_cert('certificate.cer', M2Crypto.X509.FORMAT_DER)

#pubkey = cert.get_pubkey()
#pubkey.reset_context('sha256')
#pubkey.verify_init()
#pubkey.verify_update(content)
#verified = pubkey.verify_final(signature)

import OpenSSL


import ast

cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                       open('./certificates/DATS001.crt').read())
try:
    #OpenSSL.crypto.verify(cert, signature, data, 'sha256')
    print ("Signature verified OK")
except Exception as e:
    print ("Signature verification failed: {}".format(e))


print(OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM,cert.get_pubkey()))



random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key


publickey = key.publickey()
print('public key: {}'.format(publickey))




