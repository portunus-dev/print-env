EXTS = ['.env', '.yml', '.yaml', '.json', '.js']


def get_defaults():
    return [ext if ext == '.env' else 'env{}'.format(ext) for ext in EXTS]


def is_yaml(ext):
    return ext.lower() in ('.yml', '.yaml')


def is_json(ext):
    return ext.lower() in ('.json', '.js')
