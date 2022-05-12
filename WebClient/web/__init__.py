import time
from os.path import split, realpath, exists
import logging
from configparser import ConfigParser


def get_now_path():
    return split(realpath(__file__))[0]
