try:
    from simplejson import dumps
except ImportError:
    from json import dumps

import click

from .loader import (
    load_default,
    load_file,
    load_system,
)


@click.command()
@click.version_option()
@click.option(
    '--api',
    is_flag=False,
    help='Endpoint for API sourced environment varialbes.')
@click.option(
    '-t',
    '--token',
    is_flag=False,
    help='Token for API sourced environment variables before others.')
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
    '-c',
    '--csv',
    is_flag=True,
    help='Comma instead of space separated KEY=VALUE pairs.')
@click.option(
    '-j',
    '--json',
    is_flag=True,
    help='Output in JSON string.')
@click.argument(
    'files',
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def cli(system, verbose, csv, json, files):
    delimiter = ',' if csv else ' '
    env_vars = {}

    if system:
        env_vars.update(load_system(verbose))

    if not len(files):
        env_vars.update(load_default(verbose))
    else:
        for fname in files:
            env_vars.update(load_file(fname, verbose))

    if env_vars:
        if json:
            return click.echo(dumps(env_vars))

        return click.echo(delimiter.join([
            '{0}={1}'.format(k, v) for k, v in env_vars.items()
        ]))
