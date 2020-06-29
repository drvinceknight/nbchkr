import json

def read(nb_path):
    contents = nb_path.read_text()
    nb = json.loads(contents)
    return nb
