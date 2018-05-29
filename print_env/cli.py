import click

from .loader import load_default, load_file


@click.command()
@click.version_option()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def cli(verbose, files):
    env_vars = {}

    if not len(files):
        env_vars.update(load_default(verbose))
    else:
        for fname in files:
            env_vars.update(load_file(fname, verbose))

    if env_vars:
        click.echo(' '.join([
            '{0}={1}'.format(k, v) for k, v in env_vars.items()
        ]))
