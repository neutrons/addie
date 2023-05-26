import copy
import getpass
import random
import os
import mantid.simpleapi as mantid
import datetime


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
    '''Take full path of a parent directory as the input and figure out
    an alternative directory to use. For example, if the input
    is `.`, we will be searching through the directory `.` for
    the existing directory `./output_{current_date}`. If not existing, we will
    return `./output_{current_date}` as the directory to use. If existing, we
    will append continuous integer to the end like `./output_{current_date}_{i}`
    iteratively until a certain directory does not exist when reaching a certain
    `i`. Here, the `{current_date}` represents the current date in the format of
    `mmddYYYY` such as `05252023`.
    '''

    i = 0
    date_now = datetime.datetime.now()
    date_now = date_now.strftime("%m%d%Y")
    while True:
        if i == 0:
            use_dir = os.path.join(parent_dir, f'output_{date_now}')
        else:
            use_dir = os.path.join(parent_dir, f'output_{date_now}_{i}')

        dir_exists = os.path.exists(use_dir)
        if dir_exists and len(os.listdir(use_dir)) > 0:
            i += 1
        else:
            return use_dir
