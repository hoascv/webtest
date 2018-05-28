from Crypto.Cipher import AES
import json
# Encryption
#encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# Decryption
#decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#plain_text = decryption_suite.decrypt(cipher_text)
#pycrypto

import json
import requests

data1 ={}


data1['a']='abc'
data1['b'] = 'kuno'
data = json.dumps(data1)

headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ZGVtbzpkZW1v'}
my_request = requests.post("http://ptsv2.com/t/hstest/post", json=data,headers=headers)