import os, markdown

try:
    import jinja2

    loader = jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
except ImportError:
    env = None

from dokus.document import extract_classes

def format_class(cls):
    keys = (
        'name', 'args', 'private', 'deprecated',
        'code', 'line', 'see'
    )

    data = {
        'methods': map(format_function, cls.methods),
        'desc': markdown.markdown(cls.desc.decode('utf8'))
    }

    for key in keys:
        data[key] = getattr(cls, key)

    return data

def format_function(function):
    keys = (
        'name', 'args', 'type', 'args',
        'private', 'deprecated', 'in_class',
        'code', 'line', 'see', 'basename', 'scopename'
    )

    data = {'desc': markdown.markdown(function.desc.decode('utf8'))}

    for key in keys:
        data[key] = getattr(function, key)

    return data

def render(functions, template=None):
    if template == None or isinstance(template, str):
        if env == None:
            raise ValueError('jinja2 required to using default templates')
        else:
            if template == None:
                template = 'default'

            template = env.get_template(template + '/base.html')

    classes, functions = extract_classes(functions)

    data = {
        'classes': map(format_class, classes),
        'functions': map(format_function, functions)
    }

    return template.render(data)