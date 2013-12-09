from dokus.function import Function
from dokus.util import warn, verify_identifier

def document_function(declare, filename=None):
	header = None
	args = [{'name': v, 'type': '*'} for v in declare['args']]

	function = Function(declare['name'], args)
	function.code = declare['code']
	function.line = declare['lineno']

	in_desc = False
	descriptions = []

	for comment, lineno in declare['comments']:
		comment = comment.strip()

		if comment.startswith('//') or not comment:
			continue

		if not header:
			header = _parse_header(comment, declare['name'])

			if header:
				if header['args'] != None:
					function.args = header['args']

				function.return_type = header['return_type']
			
			continue

		if not comment.startswith('@'):
			if in_desc:
				descriptions[-1] += '\n' + comment
			else:
				in_desc = True
				descriptions.append(comment)

			continue
		else:
			in_desc = False

		_interpret_prefixed(comment[1:], function, declare, filename=filename, lineno=lineno)

	if descriptions:
		function.desc = '\n\n'.join(descriptions)

	return function

def _parse_header(text, name):
	pos = text.find('(')

	if pos == -1:
		head = text
		text = ''
	else:
		head = text[:pos]
		text = text[pos + 1:]

	split = head.split()

	if len(split) > 2 or split[-1] != name:
		return

	if len(split) == 2 and split[0] != '':
		return_type = split[0]
	else:
		return_type = 'any'

	args = None

	if text != '':
		if text[-1] != ')':
			return

		args = _parse_args(text[:-1])

		if args == None:
			return

	return {'return_type': return_type, 'args': args}

def _parse_args(text):
	if not text.split():
		return []

	split = map(lambda v: v.strip(), text.split(','))
	args = []

	for item in split:
		optional = False

		if len(item) > 2 and item[0] == '[' and item[-1] == ']':
			optional = True
			item = item[1:-1]

		split_item = item.split()

		if len(split_item) > 2:
			return

		item_name = split_item[-1]
		item_type = split_item[0] if len(split_item) == 2 else 'any'

		if not verify_identifier(item_name):
			return

		args.append({
			'name': item_name,
			'type': item_type,
			'optional': optional
		})

	return args

def _interpret_prefixed(text, function, declare, filename=None, lineno=None):
	split = text.split(' ', 1)
	invalid = 'Missing content for @{} function comment'.format(split[0])
	
	if split[0] == 'return':
		if len(split) < 2:
			warn(invalid, filename=filename, lineno=lineno)
			return

		function.return_desc = split[1]

	elif split[0] == 'arg':
		split = split[1].split(' ', 1)

		if len(split) < 2:
			warn(invalid, filename=filename, lineno=lineno)
			return

		for argument in function.args:
			if argument['name'] == split[0]:
				argument['desc'] = split[1]
				break
		else:
			warn('Unknown argument for @arg function comment', filename=filename, lineno=lineno)

	elif split[0] == 'see':
		if len(split) < 2:
			warn(invalid, filename=filename, lineno=lineno)
			return

		function.see.append(split[1])

	elif split[0] == 'private':
		function.private = True
	elif split[0] == 'deprecated':
		function.deprecated = True