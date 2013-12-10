import markdown

class TSFunction(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = ''
        self.desc = ''
        self.see = []

        self.set_name_parts()

        self.private = self.infer_private()
        self.deprecated = False
        self.in_class = False
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
            'desc': markdown.markdown(self.desc.decode('utf8')),
            'args': []
        }

        for key in keys:
            data[key] = getattr(self, key)

        for arg in self.args:
            if hasattr(arg, 'desc'):
                arg['desc'] = markdown.markdown(arg['desc'].decode('utf8'))

            data['args'].append(arg)

        return data

class TSClass(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.desc = ''
        self.see = []

        self.private = self.infer_private()
        self.deprecated = False
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
        keys = ('name', 'private', 'deprecated', 'described_args',
            'code', 'line', 'see'
        )

        data = {
            'methods': [v.format() for v in self.methods],
            'desc': markdown.markdown(self.desc.decode('utf8')),
            'args': []
        }

        for key in keys:
            data[key] = getattr(self, key)

        for arg in self.args:
            if 'desc' in arg:
                arg['desc'] = markdown.markdown(arg['desc'].decode('utf8'))

            data['args'].append(arg)

        return data

    @classmethod
    def from_constructor(cls, function):
        ins = cls(function.name, function.args)
        keys = ('desc', 'see', 'private', 'deprecated', 'described_args', 'code', 'line')

        for key in keys:
            setattr(ins, key, getattr(function, key))

        return ins