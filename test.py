from dokus.declare import get_declares
from dokus.document import document_function

import os, json

def test(filename):
    with open(filename) as fp:
        text = fp.read()

    functions = [document_function(x) for x in get_declares(text)]

    result = json.dumps({
        'filename': os.path.split(filename)[1],
        'functions': [x.get_legacy_format() for x in functions],
    })

    with open(filename + '.json', 'w') as fp:
        fp.write(result)

if __name__ == '__main__':
    directory = os.path.join(os.curdir, 'tests')
    filenames = list(os.walk(directory))[0][2]

    for filename in filenames:
        if filename.endswith('.cs'):
            test(os.path.join(directory, filename))