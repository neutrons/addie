import getpass
import random

def get_ucams():
    return getpass.getuser()

def generate_random_key():
    return random.randint(0, 1e5)