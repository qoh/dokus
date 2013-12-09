from dokus.util import find_lines, verify_identifier

def get_declares(text):
    lines = find_lines(text)

    declares = []
    comments = []

    for index, (lineno, _content, start) in enumerate(lines):
        content = _content.strip()

        if content.startswith('function '):
            start += len(_content) - len(content)
            declare = _parse(text[start:])

            if declare != None:
                declare.update({
                    'start': start,
                    'index': index,
                    'lineno': lineno,
                    'comments': comments
                })

                declares.append(declare)

        if content.startswith('//'):
            comments.append(content[2:])
        else:
            comments = []

    return declares

def _parse(blob):
    size = 0

    p1 = blob.find('(')
    p2 = blob.find(')')
    p3 = blob.find('{')
    p4 = blob.find('\n')

    if p1 == -1 or p2 == -1 or p3 == -1:
        return

    if p2 < p1 or p3 < p1 or p3 < p2:
        return

    if p4 != -1 and p4 < p1:
        return

    name = blob[9:p1].rstrip()

    if not verify_identifier(name, True):
        return

    args = _parse_args(blob[p1 + 1:p2])

    if args != None:
        return {
            'name': name,
            'args': args,
            'code': blob[:p2 + 1]
        }

def _parse_args(text):
    if not text.split():
        return []

    split = map(lambda v: v.strip(), text.split(','))

    for item in split:
        if not item or item[0] != '%' or not verify_identifier(item[1:]):
            return

    return map(lambda v: v[1:], split)