def warn(text, filename=None, lineno=None):
    if filename or lineno:
        text += '[{}:{}]'.format(filename or '<input>', lineno or '?')

    print text

def find_lines(text):
    lines = []
    index = 0

    for lineno, content in enumerate(text.split('\n'), 1):
        start, index = index, index + len(content) + 1

        if content.strip():
            lines.append((lineno, content, start))

    return lines

def verify_identifier(text, allow_scope=False):
    split = text.split('::')

    if len(split) > 1 + int(allow_scope):
        return False

    normal = '_abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    for scope in split:
        if not scope:
            return False

        for index, char in enumerate(scope):
            if char.lower() not in normal and (index == 0 or char not in digits):
                return False

    return True