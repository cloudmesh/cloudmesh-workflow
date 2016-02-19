import os

def dot2svg(filename, engine='dot'):
    data = {
        'engine': engine,
        'file': filename.replace(".dot", "")
    }
    command = "{engine} -Tsvg {file}.dot > {file}.svg".format(**data)
    print(command)
    os.system(command)
