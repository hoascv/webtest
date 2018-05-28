from jinja2 import Template

def custom_function(a):
    return a.replace('o', 'ay')


with open('template.html') as report_file:
    template = report_file.read()


#template = 'Hey, my name is {{ custom_function(first_name) }}'

jinga_html_template = Template(template)
print(jinga_html_template.render(helder='kuno asdasdsad'))
#jinga_html_template.globals['custom_function'] = custom_function


