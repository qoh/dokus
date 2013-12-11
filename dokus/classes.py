try:
    from markdown import markdown
except ImportError:
    markdown = lambda v: v

class TSFunction(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = ''
        self.desc = ''

        self.fields = []
        self.see = []

        self.set_name_parts()

        self.private = self.infer_private()
        self.deprecated = False
        self.in_class = False
        self.abstract = False
        self.described_args = False

        self.code = None
        self.line = None

    def infer_private(self):
        auto = ('onadd', 'onremove')
        return self.name.startswith('_') or self.basename.lower() in auto

    def set_name_parts(self):
        split = self.name.split('::')

        self.basename = split[-1]
        self.scopename = split[0] if len(split) == 2 else ''

    def format(self):
        keys = ('name', 'basename', 'scopename', 'type',
            'private', 'deprecated', 'in_class', 'described_args',
            'code', 'line', 'see'
        )

        data = {
            'desc': markdown(self.desc.decode('utf8')),
            'args': []
        }

        for key in keys:
            data[key] = getattr(self, key)

        for arg in self.args:
            if hasattr(arg, 'desc'):
                arg['desc'] = markdown(arg['desc'].decode('utf8'))

            data['args'].append(arg)

        return data

class TSClass(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.desc = ''

        self.fields = []
        self.see = []

        self.private = self.infer_private()
        self.deprecated = False
        self.abstract = False
        self.described_args = False

        self.code = None
        self.line = None

        self.methods = []

    def infer_private(self):
        return self.name.startswith('_')

    def add_method(self, function):
        if function.in_class:
            raise ValueError()

        function.in_class = True
        self.methods.append(function)

    def format(self):
        keys = ('name', 'private', 'deprecated', 'described_args', 'code', 'line', 'see', 'abstract')

        data = {
            'methods': [v.format() for v in self.methods],
            'desc': markdown(self.desc.decode('utf8')),
            'args': [],
            'fields': []
        }

        for key in keys:
            data[key] = getattr(self, key)

        for arg in self.args:
            if 'desc' in arg:
                arg['desc'] = markdown(arg['desc'].decode('utf8'))

            data['args'].append(arg)

        for field in self.fields:
            field['desc'] = markdown(field['desc'].decode('utf8'))
            data['fields'].append(field)

        return data

    @classmethod
    def from_constructor(cls, function):
        ins = cls(function.name, function.args)
        keys = ('desc', 'see', 'private', 'deprecated', 'described_args', 'code', 'line', 'abstract', 'fields')

        for key in keys:
            setattr(ins, key, getattr(function, key))

        return ins
