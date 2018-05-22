import json
from pprint import pprint
import os, fnmatch
import requests
import webbrowser
import time
import bs4


def report():
    print("entering report")
    with open('./logs/report.html') as report_file:
        html_file = report_file.read()
        soup = bs4.BeautifulSoup(html_file,'html.parser')

        new_element = soup.new_tag("link", rel="icon", type="image/png", href="img/tor.png")





    # table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "table1")
    #
    #
    # rows = table.findAll(lambda tag: tag.name == 'tr')
    #
    # mem_attr = ['Description', 'PhysicalID', 'Slot', 'Size']
    # html = soup.find(lambda tag: tag.name == 'html')
    # table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "table1")
    # tr = table.findAll(lambda tag: tag.name == 'tr')
    # soup.append(html)
    # html.append(table)
    # table.append(tr)
    # for attr in mem_attr:
    #     tr.append('hh')






    # save the file again
    with open('./logs/report.html', "w") as outf:
        outf.write(str(soup))

    # Change path to reflect file location
    filename = 'file:///' + os.getcwd() + '/logs/' + 'report.html'

    webbrowser.open_new_tab(filename)


def send_data(data):
    start = time.time();

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    my_request = requests.post(config['server'][0]['server']+config['server'][0]['service'], json=data,
                               headers=headers)
    finish = time.time() - start

    if my_request.status_code == 201 or my_request.status_code == 409:
        pass


    # print(my_request.status_code)
    # pprint(my_request.json())

    print('status {} time elapsed {} in ms  total time: {}'.format(my_request.status_code,
                                                                   round(my_request.elapsed.total_seconds()*1000, 2),
                                                                   round(finish*1000, 2)))

    # elapsed measures the time between sending the request and finishing parsing the response headers,
    # not until the full response has been transfered.



with open('config.json') as config_file:
    config= json.load(config_file)

#with open('./data/data7.json') as data_file:
  #  data1= json.load(data_file)
 #   pprint(data1)

data_files = fnmatch.filter(os.listdir('./data'),'*.json')

for file in data_files:
    with open(config['sample_folder']+'/'+file) as data_file:
        #data = json.load(data_file)
        #pprint(json.load(data_file))
        send_data(json.load(data_file))





report()





try:
    pass
    #except Exception as e:
    #app.logger.error('Error reading bd : {}'.format(e))
except:
    pass

finally:
    pass



