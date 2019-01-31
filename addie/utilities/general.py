import getpass
import random

def get_ucams():
    return getpass.getuser()

def generate_random_key():
    return random.randint(0, 1e5)

def remove_white_spaces(str):
    return str.replace(" ", "")

def json_extractor(json=None, list_args=[]):
    if len(list_args) == 1:
        return json[list_args[0]]
    else:
        return json_extractor(json[list_args.pop(0)],
                                   list_args=list_args)
