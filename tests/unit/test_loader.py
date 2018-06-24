import os
import shutil
import json

from print_env.loader import (
    load_default,
    load_file,
    load_system,
)
from print_env.exts import (
    EXTS,
    get_defaults,
)

# patch to make FileNotFoundError "work" on Python 2.7
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


TEST_PRE = 'print_env-test'
TEMP_PRE = 'test_'
CWD = os.getcwd()


# move default files temporarily for testing no file case
def _move(back=False):
    for f in get_defaults():
        env = os.path.join(CWD, f)
        temp = os.path.join(CWD, '{0}{1}'.format(TEMP_PRE, f))
        try:
            if back:
                shutil.move(temp, env)
            else:
                shutil.move(env, temp)
        except FileNotFoundError:
            pass


def test_default_nofile():
    _move()
    assert load_default() == {}
    _move(back=True)


def test_default_files():
    _move()
    files = get_defaults()
    for ef in files:
        env_file, key, val = _write_file(ef)
        assert load_default() == {key: val}
        os.remove(env_file)
    _move(back=True)


def test_files():
    _move()
    files = ['{0}{1}'.format(TEST_PRE, ext) for ext in EXTS]
    for ef in files:
        env_file, key, val = _write_file(ef)
        assert load_file(env_file) == {key: val}
        os.remove(env_file)
    _move(back=True)


def test_system():
    env_vars = load_system()
    # test som of the most common ones
    for key in ['PWD', 'HOME', 'PATH']:
        assert key in env_vars


def test_system_with_file():
    _move()
    env_file, key, val = _write_file('{}.env'.format(TEST_PRE))
    env_vars = load_system()
    env_vars.update(load_file(env_file))
    assert env_vars.get(key) == val
    # test som of the most common ones
    for k in ['PWD', 'HOME', 'PATH']:
        assert k in env_vars
    os.remove(env_file)
    _move(back=True)


def _write_file(fname):
    env_file = os.path.join(CWD, fname)
    key = 'TEST_LOAD'
    val = 'dotenv'
    with open(env_file, 'w') as f:
        if fname.endswith(('.yml', '.yaml')):
            val = 'yaml'
            f.write('{0}: {1}\n'.format(key, val))
        elif fname.endswith(('.json', '.js')):
            val = 'json'
            json.dump({key: val}, f)
        else:
            f.write('{0}={1}\n'.format(key, val))
    return env_file, key, val
