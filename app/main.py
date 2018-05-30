import json
import os
import fnmatch
import requests
import webbrowser
import time
from app.RSAHelper import RSAHelper
from app.AESHelper import AESHelper
from app.Report import HelperReport
import base64
import sys


def encrypt_data(filename, server):

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
    payload["FileName"] = filename.split('/')[-1]
    payload["EncryptedIVString"] = base64.b64encode(iv_info).decode('utf-8')

    #print(certifi.where()) windows certificates

    with open('data.txt', 'w') as outfile:
        json.dump(payload, outfile)

    #with open('data.txt') as config_file:
    #    new_json = json.load(config_file)

    #return json.dumps(payload)
    return payload


def send_data(data, service):
    start = time.time()

    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ZGVtbzpkZW1v'}

    my_request = requests.post(service, json=data,
                               headers=headers, verify=False)

    finish = time.time() - start

    print('status {} time elapsed {} in ms  total time: {}'.format(my_request.status_code,
                                                                   round(my_request.elapsed.total_seconds()*1000, 2),
                                                                   round(finish*1000, 2)))
    # elapsed measures the time between sending the request and finishing parsing the response headers,
    # not until the full response has been transferred.

    #print("Response from server: {}".format(my_request.text))
    return {'service': service, 'time': round(my_request.elapsed.total_seconds()*1000, 2), 'message': my_request.text,
            'status_code': my_request.status_code, 'size': sys.getsizeof(data), }

############ main ###################


with open('config.json') as config_file:
    config = json.load(config_file)

report = HelperReport('./report/template.html', 'ILIAS REPORT')



"if the service active execute test"

#print(config)


for server in config['servers']:
    if server['active']:
        for service in server['services']:
            if service['active']:

                if os.path.exists(service['data_folder']):
                    data_files = fnmatch.filter(os.listdir(service['data_folder']), '*.csv')

                    for file in data_files:

                            with open(service['data_folder']+'/'+file) as data_file:
                                report.append_data((send_data(encrypt_data(data_file.name, server), server['server'] +
                                                             service['service'])), group=service['group_id'])
                else:
                    print("Directory does not exists {1} service: {0}".format(service['service_name'], service['data_folder']))

            else:
                continue

with open('./report/hsreport.html','w') as report_file:
    report_file.write(report.execute_report())


filename = 'file:///' + os.getcwd() + '/report' + '/hsreport.html'
webbrowser.open_new_tab(filename)


#try:
#    pass
        #except Exception as e:
        #app.logger.error('Error reading bd : {}'.format(e))
#except:
#    pass

#finally:
#    pass