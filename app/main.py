

import json
from pprint import pprint
import os, fnmatch
import requests
import webbrowser
import time
import bs4
from app.RSAHelper import RSAHelper
from app.AESHelper import AESHelper
import base64
from nacl.encoding import Base64Encoder
from cryptography.hazmat.primitives import serialization


def encrypt_data(file,filename):
    #TODO create a json file
    #TODO encrypt the key and IV

    enc_key = "HSKEY00000000000".encode("utf-8")

    rsa_helper = RSAHelper(config['server'][2]['pfx_certificate'], '', config['server'][2]['server_certificate'], config['server'][2]['client_key'])
    aes_helper = AESHelper(enc_key)
    key_info = rsa_helper.encrypt_info_key(aes_helper.key)
    iv_info =  rsa_helper.encrypt_info_key(aes_helper.iv)
    encrypted_string = aes_helper.encrypt(file)



    #print(base64.b64encode(key_info.decode("utf-8")))

    signature=rsa_helper.signatures(encrypted_string)

    test = base64.b64encode(signature)
    print(test)

    #print(key_info)
    #print(type(key_info))

    payload = {}

    payload["DatsId"]="0010F34DE3FA"
    payload["EncryptedKeyString"] =
    payload["VsuId"] = "a44e311e1bcc"
    #payload["RecordTime"] = "2018-04-25T12:46:07.0204193Z"
    #payload["EncryptedString"] = encrypted_string
    #payload["SignedDataString"] = base64.b64encode(signature)
    payload["FileName"] = filename
    #payload["EncryptedIVString"] = iv_info





   # with open('data.txt', 'w') as outfile:
  #     json.dump(payload, outfile)


    return json.dumps(payload)



def report():
    print("entering report")
    with open('./logs/report.html') as report_file:
        html_file = report_file.read()
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        new_element = soup.new_tag("link", rel="icon", type="image/png", href="img/tor.png")

    with open('./logs/report.html', "w") as outf:
        outf.write(str(soup))

    # Change path to reflect file location
    filename = 'file:///' + os.getcwd() + '/logs/' + 'report.html'
    webbrowser.open_new_tab(filename)


def send_data(data):
    start = time.time();

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    my_request = requests.post(config['server'][3]['server']+config['server'][3]['service'], json=data,
                               headers=headers)
    finish = time.time() - start

    if my_request.status_code == 201 or my_request.status_code == 409:
        pass

    print('status {} time elapsed {} in ms  total time: {}'.format(my_request.status_code,
                                                                   round(my_request.elapsed.total_seconds()*1000, 2),
                                                                   round(finish*1000, 2)))
    # elapsed measures the time between sending the request and finishing parsing the response headers,
    # not until the full response has been transferred.




with open('config.json') as config_file:
    config = json.load(config_file)

data_files = fnmatch.filter(os.listdir(config['features_sample_folder']), '*.csv')
for file in data_files:
    with open(config['features_sample_folder']+'/'+file) as data_file:
        encrypt_data(data_file.read(), file)

        #send_data(json.load(data_file))
        send_data(encrypt_data(data_file.read(), file))

#report()





#try:
#    pass
        #except Exception as e:
        #app.logger.error('Error reading bd : {}'.format(e))
#except:
#    pass

#finally:
#    pass