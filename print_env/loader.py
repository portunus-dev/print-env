import os
import codecs

# dotenv loader
from dotenv import dotenv_values
# yaml loader
import yaml
# json loader
try:
    import simplejson as json
except ImportError:
    import json

from .exts import EXTS, is_yaml, is_json


def load_default():
    for fname in ['.env'] + ['env{}'.format(ext) for ext in EXTS]:
        env_file = os.path.join(os.getcwd(), fname)

        if os.path.isfile(env_file):
            return load_file(env_file)
    else:
        return {}


def load_file(fname):
    try:
        _, ext = os.path.splitext(fname)

        if not is_yaml(ext) and not is_json(ext):
            return dotenv_values(fname)

        with codecs.open(fname) as f:
            if is_yaml(ext):
                return yaml.load(f)
            elif is_json(ext):
                return json.load(f)

        return {}
    except Exception:
        return {}
