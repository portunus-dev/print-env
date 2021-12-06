import os
import sys
import codecs
from setuptools import setup, find_packages
from shutil import rmtree

here = os.path.abspath(os.path.dirname(__file__))
package = "print_env"

with codecs.open(os.path.join(here, "README.md")) as f:
    long_description = "\n" + f.read()

version = {}
with codecs.open(os.path.join(here, package, "version.py")) as f:
    exec(f.read(), version)


def print_run(cmd, err_exit=False):
    print("RUNNING: {}".format(cmd))
    r = os.system(cmd)
    if err_exit and r != 0:
        sys.exit(r)


if sys.argv[-1] == "publish":
    try:
        rmtree(os.path.join(here, "dist"))
    except FileNotFoundError:
        pass

    print_run("{0} setup.py sdist bdist_wheel".format(sys.executable), True)
    print_run("env $(print-env twine.env) twine upload dist/*", True)
    print_run("git tag v{}".format(version["__version__"]))
    print_run("git push --tags")
    sys.exit()

setup(
    name="print-env",
    version=version["__version__"],
    description="CLI to print environment variables from supported sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Runzhou Li (Leo)",
    author_email="me@runzhou.li",
    url="https://github.com/woozyking/print-env",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "click>=7,<8",
        "python-dotenv==0.19.2",
        "python-gnupg==0.4.8",
        "pyyaml>=5,<6",
        "requests>=2,<3",
    ],
    entry_points={"console_scripts": ["print-env={}.cli:cli".format(package)]},
    package_data={"": ["LICENSE"]},
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
