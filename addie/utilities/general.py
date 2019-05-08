import copy
import getpass
import random
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
