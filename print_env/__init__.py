import os
import codecs

# dotenv loader
from dotenv import dotenv_values, find_dotenv
# yaml loader
import yaml
# json loader
try:
    import simplejson as json
except ImportError:
    import json


EXTS = ['env', 'yml', 'yaml', 'json']


def load_default():
    for ext in EXTS:  # try yml, yaml, json first
        env_file = os.path.join(os.getcwd(), 'env.{}'.format(ext))

        if os.path.isfile(env_file):
            break
    else:  # then resort to .env
        env_file = find_dotenv()

    if env_file:
        return load_file(env_file)

    return {}


def load_file(fname):
    try:
        _, ext = os.path.splitext(fname)

        if not is_yaml(ext) and not is_json(ext):
            return dotenv_values(fname)

        with codecs.open(fname, encoding='utf-8') as f:
            if is_yaml(ext):
                return yaml.load(f)
            elif is_json(ext):
                return json.load(f)

        return {}
    except Exception:
        return {}


def is_yaml(ext):
    return ext.lower() in ('.yml', '.yaml')


def is_json(ext):
    return ext.lower() in ('.json', '.js')
