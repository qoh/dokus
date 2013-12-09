try:
    import jinja2

    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
except ImportError:
    env = None

def format_function(function):
    keys = (
        'name', 'args', 'desc', 'private', 'deprecated',
        'return_type', 'return_desc', 'code', 'line', 'see'
    )

    data = {}

    for key in keys:
        data[key] = getattr(function, key)

    return data

def render(functions, template=None):
    if template == None or isinstance(template, basestr):
        if env == None:
            raise ValueError('jinja2 required to using default templates')
        else:
            if template == None:
                template = 'default.html'

            template = env.get_template(template)

    normals = []
    specials = []

    for function in functions:
        format = format_function(function)

        if function.private or function.deprecated:
            specials.append(format)
        else:
            normals.append(format)

    data = {
        'functions': normals or None,
        'functions_special': specials or None
    }

    return template.render(data)