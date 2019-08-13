import os
import codecs

# dotenv loader
from dotenv import dotenv_values
# yaml loader
import yaml
try:
    from yaml import CLoader as YLoader
except ImportError:
    from yaml import Loader as YLoader
# json loader
try:
    import simplejson as json
except ImportError:
    import json
# API loader - requests
import requests
# GnuPG for decrypting encrypted API loaded env vars
import gnupg

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
                    env_vars = yaml.load(f, Loader=YLoader)
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
        secho(msg='Sourced system environment variables', lvl='debug')

    return dict(os.environ)


def load_api(api, token, verbose=False):
    env_vars = {}

    try:
        jwt, project_id, stage = token.split('/')
    except ValueError:
        if verbose:
            secho(msg='Invalid token', lvl='error')

        return env_vars

    r = requests.get(api, params={'project_id': project_id, 'stage': stage})

    if r.status_code != 200:
        if verbose:
            try:
                err = r.json()
                err = err.get('message', err)
            except Exception:
                err = r.text

            secho(msg='API error - {}'.format(err), lvl='error')

        return env_vars

    try:
        data = r.json()
        encrypted = data.get('encrypted', False)
        env_vars = data.get('vars', {})

        if encrypted:
            gpg = gnupg.GPG()
            env_vars = json.loads(str(gpg.decrypt(env_vars)))

        if verbose:
            if not env_vars:
                secho(
                    msg='Sourced from invalid API {}'.format(api),
                    lvl='warning'
                )
            else:
                secho(msg='Sourced from API {}'.format(api), lvl='debug')
    except Exception as e:
        if verbose:
            secho(msg='API error - {}'.format(e), lvl='error')

        env_vars = {}

    return env_vars
