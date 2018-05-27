from print_env.exts import is_yaml, is_json


def test_is_yaml():
    cases = {
        '.yml': True,
        '.yaml': True,
        '.json': False,
        '.js': False,
        '.env': False
    }
    for k, v in cases.items():
        assert is_yaml(k) is v


def test_is_json():
    cases = {
        '.yml': False,
        '.yaml': False,
        '.json': True,
        '.js': True,
        '.env': False
    }
    for k, v in cases.items():
        assert is_json(k) is v
