from dokus.util import warn, find_lines, verify_identifier

def get_declares(text, filename=None):
    lines = find_lines(text)

    declares = []
    comments = []

    for index, (lineno, _content, start) in enumerate(lines):
        content = _content.strip()

        if content.startswith('function '):
            start += len(_content) - len(content)
            declare = _parse(text[start:], filename, lineno)

            if declare != None:
                declare.update({
                    'start': start,
                    'index': index,
                    'lineno': lineno,
                    'comments': comments
                })

                declares.append(declare)

        if content.startswith('//'):
            comments.append((content[2:], lineno))
        else:
            comments = []

    return declares

def _parse(blob, filename=None, lineno=None):
    size = 0

    p1 = blob.find('(')
    p2 = blob.find(')')
    p3 = blob.find('{')
    p4 = blob.find('\n')

    if p1 == -1 or p2 == -1 or p3 == -1:
        warn('Invalid function declaration - missing tokens', filename=filename, lineno=lineno)
        return

    if p2 < p1 or p3 < p1 or p3 < p2 or (p4 != -1 and p4 < p1):
        warn('Invalid function declaration - wrong token order', filename=filename, lineno=lineno)
        return

    name = blob[9:p1].rstrip()

    if not verify_identifier(name, True):
        warn('Invalid identifier \'{}\''.format(name), filename=filename, lineno=lineno)
        return

    args = _parse_args(blob[p1 + 1:p2])

    if args and '::' in name:
        args = args[1:]

    if args != None:
        return {
            'name': name,
            'args': args,
            'code': blob[:p2 + 1]
        }

    warn('Invalid argument list', filename=filename, lineno=lineno)

def _parse_args(text):
    if not text.split():
        return []

    split = map(lambda v: v.strip(), text.split(','))

    for item in split:
        if not item or item[0] != '%' or not verify_identifier(item[1:]):
            return

    return map(lambda v: v[1:], split)