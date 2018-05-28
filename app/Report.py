from jinja2 import Template
import webbrowser
import os

class HelperReport(object):
    def __init__(self, template_path, name):
        self.template = template_path
        self.name = name
        self.data = {'report': name, 'service': []}

    def report(self, table, value):
        pass

    def append_data(self,data,):
        self.data['service'].append(data)

    def execute_report(self):
        with open(self.template) as report_file:
            template = report_file.read()

        jinga_html_template = Template(template)

        return jinga_html_template.render(name=self.name, data=self.data)

