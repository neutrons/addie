import copy
import getpass
import random
import os
import mantid.simpleapi as mantid


def get_ucams():
    return getpass.getuser()


def generate_random_key():
    return random.randint(0, 1e5)


def remove_white_spaces(str):
    return str.replace(" ", "")


def json_extractor(json=None, list_args=[]):

    json = copy.deepcopy(json)
    list_args = copy.deepcopy(list_args)

    try:
        if len(list_args) == 1:
            return json[list_args[0]]
        else:
            return json_extractor(json[list_args.pop(0)],
                                  list_args=list_args)
    except KeyError:
        return "N/A"


def get_list_algo(algo_name):
    _alg = mantid.AlgorithmManager.createUnmanaged(algo_name)
    _alg.initialize()
    list_algo = [prop.name for prop in _alg.getProperties()]
    return list_algo


def config_dir_to_use(parent_dir):
    # Take full path of a parent directory as the input and figure out
    # an alternative directory to use. For example, if the input
    # is `.`, we will be searching through the directory `.` for 
    # existing directories like `./output`, `./output_1`, `./output_2`, ...
    # until a certain `./output_i` is not existing.

    i = 0
    while True:
        if i == 0:
            use_dir = os.path.join(parent_dir, 'output')
        else:
            use_dir = os.path.join(parent_dir, f'output_{i}')

        dir_exists = os.path.exists(use_dir)
        if dir_exists:
            i += 1
        else:
            return use_dir
