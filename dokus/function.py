class Function(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args

        self.desc = None
        self.see = []

        self.private = name.startswith('_')
        self.deprecated = False

        self.return_type = 'any'
        self.return_desc = None

        self.code = None
        self.line = None

    def get_legacy_format(self):
        return {
            'name': self.name,
            'args': self.args,
            'desc': self.desc,
            'return_type': self.return_type,
            'return_desc': self.return_desc,
            'code': self.code_text,
            'line': self.code_line,
            'see': self.see or None
        }