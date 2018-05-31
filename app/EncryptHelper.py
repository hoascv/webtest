from app.RSAHelper import RSAHelper
from app.AESHelper import AESHelper
import json
import base64
import uuid
import os


class Encrypt(object):
    def __init__(self):
        pass

    @staticmethod
    def encrypt_data(filename, server, vsu=False, debug=False):

        enc_key = "HSKEY00000000000".encode("utf-8")
        rsa_helper = RSAHelper(server['pfx_certificate'], '', server['server_certificate'], server['client_key'])
        aes_helper = AESHelper(enc_key)
        key_info = rsa_helper.encrypt_info_key(aes_helper.key)
        iv_info = rsa_helper.encrypt_info_key(aes_helper.iv)

        with open(filename, "r") as file_data:
            content = file_data.read()

        encrypted_string = aes_helper.encrypt(content)

        signature = rsa_helper.signatures(encrypted_string)

        payload = {}
        payload["DatsId"] = "a44e311e1bcc"
        payload["EncryptedKeyString"] = base64.b64encode(key_info).decode('utf-8')
        payload["VsuId"] = "a44e311e1bcc"
        payload["RecordTime"] = "2018-04-25T12:46:07.0204193Z"
        payload["EncryptedString"] = base64.b64encode(encrypted_string).decode('utf-8')
        payload["SignedDataString"] = base64.b64encode(signature).decode('utf-8')
        payload["FileName"] = filename.split('\\')[-1]
        payload["EncryptedIVString"] = base64.b64encode(iv_info).decode('utf-8')

        if vsu:
            pass
            #include batch ID

        if debug:
            debug_file_name = str(uuid.uuid4())
            debug_path = server['debug_payload_folder']
            if os.path.exists(debug_path):
                with open(debug_path + '/' + debug_file_name, 'w') as outfile:
                    json.dump(payload, outfile)
            else:
                print("Directory does not exists {} Check config file for the service".format(debug_path))

        return payload
