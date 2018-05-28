import json
import os
import fnmatch
import requests
import webbrowser
import time
import bs4
from app.RSAHelper import RSAHelper
from app.AESHelper import AESHelper
import base64
import certifi
import ssl


def encrypt_data(filename):

    enc_key = "HSKEY00000000000".encode("utf-8")
    rsa_helper = RSAHelper(config['server'][2]['pfx_certificate'], '', config['server'][2]['server_certificate'], config['server'][2]['client_key'])
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
    payload["FileName"] = filename.split('/')[-1]
    payload["EncryptedIVString"] = base64.b64encode(iv_info).decode('utf-8')

    #print(certifi.where()) windows certificates

    with open('data.txt', 'w') as outfile:
        json.dump((payload), outfile)

    #with open('data.txt') as config_file:
    #    new_json = json.load(config_file)

    #return json.dumps(payload)
    return payload


def report():







def send_data(data, service):
    start = time.time()

    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ZGVtbzpkZW1v'}

    my_request = requests.post(service, json=data,
                               headers=headers, verify=False)

    finish = time.time() - start

    if my_request.status_code == 201 or my_request.status_code == 409:
        pass

    print('status {} time elapsed {} in ms  total time: {}'.format(my_request.status_code,
                                                                   round(my_request.elapsed.total_seconds()*1000, 2),
                                                                   round(finish*1000, 2)))
    # elapsed measures the time between sending the request and finishing parsing the response headers,
    # not until the full response has been transferred.

    print("Response from server: {}".format(my_request.text))
    return {'service': service, 'time': round(my_request.elapsed.total_seconds()*1000, 2)}
# main

with open('config.json') as config_file:
    config = json.load(config_file)
report = {'date': 'date',  'server': [],}

data_files = fnmatch.filter(os.listdir(config['features_sample_folder']), '*.csv')
vsu_health_files = fnmatch.filter(os.listdir(config['health_sample_folder']), 'vsu_*.csv')
dats_health_files = fnmatch.filter(os.listdir(config['health_sample_folder']), 'dats_*.csv')

for file in data_files:
    with open(config['features_sample_folder']+'/'+file) as data_file:
        pass
        #report['server'].append(send_data(encrypt_data(data_file.name), config['server'][3]['server']+config['server'][3]['feature_service']))

for file in vsu_health_files:
    with open(config['health_sample_folder'] + '/' + file) as data_file:
        report['server'].append(send_data(encrypt_data(data_file.name), config['server'][3]['server']+config['server'][3]['vsu_health_service']))
        print(data_file.name)

for file in dats_health_files:
    with open(config['health_sample_folder'] + '/' + file) as data_file:
        report['server'].append(send_data(encrypt_data(data_file.name), config['server'][3]['server']+config['server'][3]['dats_health_service']))
        print(data_file.name)


print(report)


#report()





#try:
#    pass
        #except Exception as e:
        #app.logger.error('Error reading bd : {}'.format(e))
#except:
#    pass

#finally:
#    pass