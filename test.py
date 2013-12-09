from dokus.declare import get_declares
from dokus.document import document_function
from dokus.render import render

import os, json

def test(filename):
    basename = os.path.split(filename)[1]

    with open(filename) as fp:
        text = fp.read()

    functions = [document_function(x, basename) for x in get_declares(text, basename)]

    with open(filename + '.html', 'w') as fp:
        fp.write(render(functions))

if __name__ == '__main__':
    directory = os.path.join(os.curdir, 'tests')
    filenames = list(os.walk(directory))[0][2]

    for filename in filenames:
        if filename.endswith('.cs'):
            test(os.path.join(directory, filename))