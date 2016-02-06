import os
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

template_dir = os.path.dirname(__file__)

def index(context_dict = {}):
    index_html = ""
    try:
        f_path = os.path.join(template_dir, 'index.html')
        with open(f_path) as f:
            index_html = f.read()
            #usar regex para mudar o template
    except Exception as e:
        print e
    return index_html

def template(filename, context_dict = {}):
    env = Environment()
    env.loader = FileSystemLoader(template_dir)
    try:
        template = env.get_template(filename)
        return template.render(context_dict)
    except Exception as e:
        print "Template"
        print e
        return None
