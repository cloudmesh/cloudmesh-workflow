import os

def dot2svg(filename, engine='dot'):
    data = {
        'engine': engine,
        'file': filename.replace(".dot", "")
    }
    command = "{engine} -Tsvg {file}.dot > {file}.svg".format(**data)
    print(command)
    os.system(command)


def browser(filename):
    data = {
        'engine': 'python -m webbrowser',
        'file': filename
    }
    if 'file:' not in filename and 'http' not in filename:
        os.system("python -m webbrowser -t file:///{file}".format(**data))
    else:
        os.system("python -m webbrowser -t {file}".format(**data))