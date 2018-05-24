import os
import sys
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
package = 'print_env'

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with codecs.open(os.path.join(here, package, '.ver'), encoding='utf-8') as f:
    version = f.read().strip()

def print_run(cmd):
    print('RUNNING: {}'.format(cmd))
    os.system(cmd)

if sys.argv[-1] == 'publish':
    print_run('{0} setup.py sdist bdist_wheel'.format(sys.executable))
    print_run('twine upload dist/*')
    print_run('git tag v{}'.format(version))
    print_run('git push --tags')
    sys.exit()

required = [
    'python-dotenv',
    'pyyaml',
    'click'
]

setup(
    name='print-env',
    version=version,
    description='CLI to print environment variables from supported files.',
    long_description=long_description,
    author='Runzhou Li (Leo)',
    author_email='me@runzhou.li',
    url='https://github.com/woozyking/print-env',
    packages=find_packages(exclude=['tests']),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'print-env={}.cli:cli'.format(package)
        ]
    },
    package_data={
        '': ['LICENSE', '{}/.ver'.format(package)]
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
