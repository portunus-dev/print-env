EXTS = ['.env', '.yml', '.yaml', '.json', '.js']


def is_yaml(ext):
    return ext.lower() in ('.yml', '.yaml')


def is_json(ext):
    return ext.lower() in ('.json', '.js')
