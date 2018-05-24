import click

from . import load_default, load_file


@click.command()
@click.version_option()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def cli(files):
    env_vars = {}

    if not len(files):
        env_vars.update(load_default())
    else:
        for fname in files:
            env_vars.update(load_file(fname))

    if env_vars:
        click.echo(' '.join([
            '{0}={1}'.format(k, v) for k, v in env_vars.items()
        ]))
