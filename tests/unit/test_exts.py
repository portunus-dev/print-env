from print_env.exts import (
    EXTS,
    get_defaults,
    is_yaml,
    is_json,
)


def test_get_defaults():
    defaults = get_defaults()
    for f in defaults:
        assert f.endswith(tuple(EXTS))


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
