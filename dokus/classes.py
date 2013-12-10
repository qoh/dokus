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

        self.code = None
        self.line = None

    def infer_private(self):
        auto = ('onadd', 'onremove')
        return self.name.startswith('_') or self.basename.lower() in auto

    def set_name_parts(self):
        split = self.name.split('::')

        self.basename = split[-1]
        self.scopename = split[0] if len(split) == 2 else ''

class TSClass(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.desc = ''
        self.see = []

        self.private = self.infer_private()
        self.deprecated = False

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

    @classmethod
    def from_constructor(cls, function):
        ins = cls(function.name, function.args)
        keys = ('desc', 'see', 'private', 'deprecated', 'code', 'line')

        for key in keys:
            setattr(ins, key, getattr(function, key))

        return ins