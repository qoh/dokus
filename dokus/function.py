class Function(object):
	#TODO

	def __init__(self, declare):
		self.declare = declare

	def get_legacy_format(self):
		return {
            'name': self.declare['name'],
            'args': [{'name': v, 'type': '*'} for v in self.declare['args']],
            'code': {'code': self.declare['code'], 'lineno': self.declare['lineno']},
            'desc': '\n'.join(self.declare['comments'])
        }