from Crypto.Cipher import AES
import json
# Encryption
#encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# Decryption
#decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#plain_text = decryption_suite.decrypt(cipher_text)
#pycrypto



pythonDictionary = {'name':'Bob', 'age':44, 'isEmployed':True}
dictionaryToJson = json.dumps(pythonDictionary)
print (dictionaryToJson)