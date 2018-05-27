import os
import shutil
import json

from print_env.loader import load_default, load_file

# patch to make FileNotFoundError "work" on Python 2.7
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


FILES = ['.env', 'env.yml', 'env.json']
TEMP_PRE = 'test_'
CWD = os.getcwd()


# move default files temporarily for testing no file case
def _move(back=False):
    for f in FILES:
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


def test_default_dotenv():
    _move()
    env_file = os.path.join(CWD, '.env')
    key = 'TEST_LOAD'
    val = 'dotenv'
    with open(env_file, 'w') as f:
        f.write('{0}={1}\n'.format(key, val))
    assert load_default() == {key: val}
    os.remove(env_file)
    _move(back=True)


def test_default_yaml():
    _move()
    for ef in ('env.yml', 'env.yaml'):
        env_file = os.path.join(CWD, ef)
        key = 'TEST_LOAD'
        val = 'yaml'
        with open(env_file, 'w') as f:
            f.write('{0}: {1}\n'.format(key, val))
        assert load_default() == {key: val}
        os.remove(env_file)
    _move(back=True)


def test_default_json():
    _move()
    for ef in ('env.js', 'env.json'):
        env_file = os.path.join(CWD, ef)
        key = 'TEST_LOAD'
        val = 'json'
        with open(env_file, 'w') as f:
            json.dump({key: val}, f)
        assert load_default() == {key: val}
        os.remove(env_file)
    _move(back=True)


def test_file_dotenv():
    _move()
    env_file = os.path.join(CWD, 'test.env')
    key = 'TEST_LOAD'
    val = 'dotenv'
    with open(env_file, 'w') as f:
        f.write('{0}={1}\n'.format(key, val))
    assert load_file(env_file) == {key: val}
    os.remove(env_file)
    _move(back=True)


def test_file_yaml():
    _move()
    for ef in ('test-env.yml', 'test-env.yaml'):
        env_file = os.path.join(CWD, ef)
        key = 'TEST_LOAD'
        val = 'yaml'
        with open(env_file, 'w') as f:
            f.write('{0}: {1}\n'.format(key, val))
        assert load_file(env_file) == {key: val}
        os.remove(env_file)
    _move(back=True)


def test_file_json():
    _move()
    for ef in ('test-env.js', 'test-env.json'):
        env_file = os.path.join(CWD, ef)
        key = 'TEST_LOAD'
        val = 'json'
        with open(env_file, 'w') as f:
            json.dump({key: val}, f)
        assert load_file(env_file) == {key: val}
        os.remove(env_file)
    _move(back=True)
