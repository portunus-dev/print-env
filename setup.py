import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

required = [
    'python-dotenv',
    'pyyaml',
    'click'
]

setup(
    name='print-env',
    version='0.1',
    description='CLI to print environment variables from supported files.',
    long_description=long_description,
    author='Runzhou Li (Leo)',
    author_email='me@runzhou.li',
    url='https://github.com/woozyking/print-env',
    packages=find_packages(exclude=['tests']),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'print-env=print_env.cli:cli'
        ]
    },
    package_data={
        '': ['LICENSE']
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
