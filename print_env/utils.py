from click import secho as echo


COLOR_MAP = {
    'error': 'red',
    'fatal': 'red',
    'warning': 'yellow'
}


def secho(**kwargs):
    lvl = kwargs.get('lvl', 'debug')
    msg = kwargs.get('msg', '')
    loader = kwargs.get('loader', 'Default')

    if msg:
        echo(
            '[{lvl}][{loader}]\t{msg}'.format(
                lvl=lvl.upper(), loader=loader.upper(), msg=msg
            ),
            fg=COLOR_MAP.get(lvl.lower(), 'cyan'),
            err=True  # workaround to print but not to env var output
        )
