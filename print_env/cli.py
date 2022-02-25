import os
from json import dumps

import click

from .loader import (
    load_default,
    load_file,
    load_system,
    load_api,
)


@click.command()
@click.version_option()
@click.option(
    '--api',
    is_flag=False,
    default='https://cli.mindswire.com/env',
    help='Endpoint for API sourced environment varialbes.')
@click.option(
    '-t',
    '--token',
    is_flag=False,
    help='Token for API sourced environment variables before others.')
@click.option(
    '--team',
    is_flag=False,
    help='Team for API sourced environment variables.')
@click.option(
    '--project',
    is_flag=False,
    help='Project for API sourced environment variables.')
@click.option(
    '--stage',
    is_flag=False,
    default=None,
    help='Stage for API sourced environment variables.')
@click.option(
    '--no_default',
    is_flag=True,
    help='Do not load from default local file(s).')
@click.option(
    '-s',
    '--system',
    is_flag=True,
    help='Load system environment variables before local ones.')
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    help='Enables verbose mode.')
@click.option(
    '-f',
    '--format',
    is_flag=False,
    type=click.Choice(['space', 'csv', 'newline', 'json']),
    default='space',
    help='Output format.')
@click.option(  # deprecated, use --format
    '-c',
    '--csv',
    is_flag=True,
    help='Comma instead of space separated KEY=VALUE pairs. DEPRECIATED, use --format csv.')
@click.option(  # deprecated, use --format
    '-j',
    '--json',
    is_flag=True,
    help='Output in JSON string. DEPRECATED, use --format=json.')
@click.argument(
    'files',
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def cli(api, token, team, project, stage, no_default, system, verbose, format, csv, json, files):
    env_vars = {}

    if system:
        env_vars.update(load_system(verbose))

    if not len(files):
        if not no_default:
            env_vars.update(load_default(verbose))
    else:
        for fname in files:
            env_vars.update(load_file(fname, verbose))

    token = token or env_vars.pop('PORTUNUS_TOKEN', os.getenv('PORTUNUS_TOKEN'))
    if token:
        copy = env_vars.copy()
        api_envs = load_api(
            api=api,
            team=team,
            project=project,
            token=token,
            stage=stage,
            verbose=verbose,
        )
        env_vars.update(api_envs)
        # TODO: let user control the precedence of these env vars
        env_vars.update(copy)

    if env_vars:
        if json or format == 'json':
            return click.echo(dumps(env_vars))

        delimiter = ' '
        if csv or format == 'csv':
            delimiter = ','
        elif format == 'newline':
            delimiter = '\n'

        return click.echo(delimiter.join([
            '{0}={1}'.format(k, v) for k, v in env_vars.items()
        ]))
