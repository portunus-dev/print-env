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

from .exts import (
    get_defaults,
    is_yaml,
    is_json,
)
from .utils import secho


def load_default(verbose=False):
    cwd = os.getcwd()
    defaults = get_defaults()

    for fname in defaults:
        env_file = os.path.join(cwd, fname)

        if os.path.isfile(env_file):
            return load_file(env_file, verbose)
    else:
        if verbose:
            secho(
                msg='No default ({ds}) found at {cwd}/'.format(
                    ds=', '.join(defaults),
                    cwd=cwd
                ).strip(),
                lvl='warning'
            )

        return {}


def load_file(fname, verbose=False):
    env_vars = {}

    try:
        _, ext = os.path.splitext(fname)

        if not is_yaml(ext) and not is_json(ext):
            env_vars = dotenv_values(fname)
        else:
            with codecs.open(fname) as f:
                if is_yaml(ext):
                    env_vars = yaml.load(f, Loader=yaml.FullLoader)
                elif is_json(ext):
                    env_vars = json.load(f)

        if verbose:
            if not env_vars:
                secho(
                    msg='Sourced from invalid file {}'.format(fname),
                    lvl='warning'
                )
            else:
                secho(msg='Sourced from file {}'.format(fname), lvl='debug')
    except Exception as e:
        if verbose:
            secho(
                msg='Failed to load file {f}\n{e}'.format(
                    f=fname,
                    e=e
                ),
                lvl='error'
            )

    return env_vars


def load_system(verbose=False):
    if verbose:
        secho(msg='Sourced system environment variables')

    return dict(os.environ)
