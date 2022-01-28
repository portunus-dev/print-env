import os
import codecs
# json loader
import json
from xmlrpc.client import Boolean

# dotenv loader
from dotenv import dotenv_values
# yaml loader
import yaml
try:
    from yaml import CLoader as YLoader
except ImportError:
    from yaml import Loader as YLoader
# API loader - requests
import requests
# GnuPG for decrypting encrypted API loaded env vars
import gnupg

from print_env.exts import (
    get_defaults,
    is_yaml,
    is_json,
)
from print_env.utils import secho


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


def load_file(fname, verbose=False) -> dict:
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
                    msg='Invalid file {}'.format(fname),
                    lvl='warning',
                    loader='file'
                )
            else:
                secho(
                    msg='From file {}'.format(fname),
                    lvl='debug',
                    loader='file'
                )
    except Exception as e:
        if verbose:
            secho(
                msg='Failed to load {f}\n{e}'.format(
                    f=fname,
                    e=e
                ),
                lvl='error',
                loader='file'
            )

    return env_vars


def load_system(verbose=False):
    if verbose:
        secho(
            msg='From system environment variables',
            lvl='debug',
            loader='system'
        )

    return dict(os.environ)


def load_api(api: str, token: str, stage: str = None, verbose: Boolean = False) -> dict:
    env_vars = {}
    try:
        token_parts = token.split('/')
        jwt = token_parts[0]
        project = token_parts[1]
        _stage = None
        if len(token_parts) == 3 and token_parts[2]:
            _stage = token_parts[2]
    except ValueError:
        if verbose:
            secho(msg='Invalid token', lvl='error', loader='API')

        return env_vars

    stage = stage or _stage

    if not stage:
        if verbose:
            secho(msg='No stage specified', lvl='error', loader='API')

        return env_vars

    params = dict(project=project, stage=stage, encrypt=0)
    r = requests.get(api, params=params, headers={'portunus-jwt': jwt})

    if r.status_code != 200:
        if verbose:
            try:
                err = r.json()
                err = err.get('message', err)
            except Exception:
                err = r.text

            secho(msg='API error - {}'.format(err), lvl='error', loader='API')

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
                    msg=f'No vars loaded for project {project} ({stage})',
                    lvl='warning',
                    loader='API'
                )
            else:
                secho(
                    msg='Project {} (Stage: {}, Encrypted: {})'.format(
                        project, stage, encrypted),
                    lvl='debug',
                    loader='API'
                )
    except Exception as e:
        if verbose:
            secho(msg='API error - {}'.format(e), lvl='error', loader='API')

        env_vars = {}

    return env_vars
