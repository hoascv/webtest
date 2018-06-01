from jinja2 import Template
import webbrowser
import os
from datetime import datetime
from tzlocal import get_localzone


class HelperReport(object):
    def __init__(self, template_path, name):
        self.template = template_path
        self.data = {"report": name, "service": [{"content": []}, {"content": []}, {"content": []}]}
        self.report_date = datetime.now(get_localzone())
        self.finish=0
        
    def report(self, table, value):
        pass

    def append_data(self, data, group):
        return self.data['service'][group]['content'].append(data)

    def report_finish(self, finish):
        self.finish = finish
        #self.data['service'][table].append(data)

    def execute_report(self):
        with open(self.template) as report_file:
            template = report_file.read()

        jinga_html_template = Template(template)

        return jinga_html_template.render(data=self.data, size=len(self.data['service']), date=self.report_date, finish=self.finish)

