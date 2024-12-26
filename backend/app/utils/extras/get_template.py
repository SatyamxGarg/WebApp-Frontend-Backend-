from jinja2 import Environment, FileSystemLoader

def get_template(template_name: str):
    env = Environment(loader=FileSystemLoader('templates'))
    return env.get_template(template_name)