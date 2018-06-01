from threading import Thread
import threading
import time
import logging
from random import randint
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
import time


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
lock = threading.Lock()
report = HelperReport('./report/template.html', 'ILIAS REPORT')


class DATS(Thread):

    def __init__(self, target=None, name=None, dats_id=None, kwargs=None):
        super().__init__(name=name, target=target, )

        self.kwargs = kwargs
        self.dats_id = dats_id

    def encrypt_data(self, filename, server):

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
        payload["DatsId"] = self.dats_id
        payload["EncryptedKeyString"] = base64.b64encode(key_info).decode('utf-8')
        payload["VsuId"] = self.kwargs['vsu']
        payload["RecordTime"] = "2018-04-25T12:46:07.0204193Z"
        payload["EncryptedString"] = base64.b64encode(encrypted_string).decode('utf-8')
        payload["SignedDataString"] = base64.b64encode(signature).decode('utf-8')
        payload["FileName"] = filename.split('\\')[-1]
        payload["EncryptedIVString"] = base64.b64encode(iv_info).decode('utf-8')



        with open('data.txt', 'w') as outfile:
            json.dump(payload, outfile)

        #with open('data.txt') as config_file:
        #    new_json = json.load(config_file)

        #return json.dumps(payload)
        return payload

    def send_data(self, data, service, request_id):
        start = time.time()

           #teste
        if threading.current_thread().name == 'DATS00001' :
            time.sleep(5)

        headers = {'Content-type': 'application/json', 'Accept': 'application/json',
                   'Authorization': 'Basic ZGVtbzpkZW1v'}

        my_request = requests.post(service, json=data,
                                   headers=headers, verify=False)

        finish = time.time() - start

        print('status {} time elapsed {} (ms)  total time: {} message {} Request id {} filename {}'.format(
            my_request.status_code,
            round(my_request.elapsed.total_seconds() * 1000, 2),
            round(finish * 1000, 2), my_request.text, request_id, data['FileName']))
        # elapsed measures the time between sending the request and finishing parsing the response headers,
        # not until the full response has been transferred.

        # print("Response from server: {}".format(my_request.text))
        return {'service': service, 'time': round(my_request.elapsed.total_seconds() * 1000, 2),
                'message': my_request.text,
                'status_code': my_request.status_code, 'size': sys.getsizeof(data), 'filename': data['FileName'],
                'request_id': request_id}

    def process(self):


        with open('config.json') as config_file:
            config = json.load(config_file)





        "if the service active execute test"


        request_number=1


        for server in config['servers']:
            if server['active']:
                for service in server['services']:
                    if service['active']:

                        if os.path.exists(service['data_folder']):

                            for root, dirs, files in os.walk(service['data_folder']):
                                for filename in fnmatch.filter(files, '*.csv'):
                                    full_path = os.path.join(root, filename)
                                    with open(full_path) as data_file:
                                        request_response = self.send_data(self.encrypt_data(data_file.name, server),
                                                                          server['server'] +
                                                                          service['service'], request_id=threading.current_thread().name + '[' + str(request_number) +']')

                                        #
                                        lock.acquire()
                                        report.append_data(request_response, group=service['group_id'])
                                        lock.release()
                                        request_number += 1
                        else:
                            logging.ERROR("Directory does not exists {1} service: {0}".format(service['service_name'],
                                                                                              service['data_folder']))

                    else:
                        continue


        return

    def run(self):

        logging.debug('running with %s and %s', self.dats_id, self.kwargs)
        self.process()
        return


def main():
    requests_start = time.time()

    for i in range(2):
        t_worker = DATS(name='DATS' + str(i).zfill(4), dats_id="0001C0099AEA", kwargs={'vsu': 'a44e311e1bcc'})
        t_worker.start()

    t_worker.join()

    report.report_finish(time.time() - requests_start)
    with open('./report/hsreport.html', 'w') as report_file:
        report_file.write(report.execute_report())

    filename = 'file:///' + os.getcwd() + '/report' + '/hsreport.html'
    webbrowser.open_new_tab(filename)


if __name__ == '__main__':
    main()
