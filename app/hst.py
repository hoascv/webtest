
from jinja2 import Template
import webbrowser
import os

data1 ={'server':[]}

data1['server'].append({'name':'helder', 'idade':36 })
data1['server'].append({'name':'louise', 'idade':40 })
data1['server'].append({'name':'Thomas', 'idade':3 })


with open('template.html') as report_file:
    template = report_file.read()

jinga_html_template = Template(template)

hh= jinga_html_template.render(helder='hoas',data=data1)

print(hh)
with open('hsreport.html','w') as report:
    report.write(hh)



filename = 'file:///' + os.getcwd()  + '/hsreport.html'
webbrowser.open_new_tab(filename)

#webbrowser.open_new_tab('hsreport.html')




#headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ZGVtbzpkZW1v'}
#my_request = requests.post("http://ptsv2.com/t/hstest/post", json=data,headers=headers)