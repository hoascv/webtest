from jinja2 import Template
import webbrowser
import os


class HelperReport(object):
    def __init__(self, template_path, name):
        self.template = template_path
        self.data = {"report": name, "service": [{"content": []}, {"content": []}, {"content": []}]

}

    def report(self, table, value):
        pass

    def append_data(self, data, group):
        return self.data['service'][group]['content'].append(data)



        #self.data['service'][table].append(data)

    def execute_report(self):
        with open(self.template) as report_file:
            template = report_file.read()

        jinga_html_template = Template(template)

        return jinga_html_template.render(data=self.data, size=len(self.data['service']))

