#!/usr/bin/env python

from __future__ import absolute_import, print_function

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

NAME = "future"
PACKAGES = [
    "future",
    "future.builtins",
    "future.types",
    "future.standard_library",
    "future.backports",
    "future.backports.email",
    "future.backports.email.mime",
    "future.backports.html",
    "future.backports.http",
    "future.backports.test",
    "future.backports.urllib",
    "future.backports.xmlrpc",
    "future.moves",
    "future.moves.dbm",
    "future.moves.html",
    "future.moves.http",
    "future.moves.test",
    "future.moves.tkinter",
    "future.moves.urllib",
    "future.moves.xmlrpc",
    "future.tests",
    "future.utils",
    "past",
    "past.builtins",
    "past.types",
    "past.utils",
    "past.translation",
    "libfuturize",
    "libfuturize.fixes",
    "libpasteurize",
    "libpasteurize.fixes",
]

if sys.version_info[:2] < (3, 0):
    PACKAGES += [
        "builtins",
        "copyreg",
        "html",
        "http",
        "queue",
        "reprlib",
        "socketserver",
        "tkinter",
        "winreg",
        "xmlrpc",
        "_dummy_thread",
        "_markupbase",
        "_thread",
    ]

PACKAGE_DATA = {
    '': [
        'README.rst',
        'LICENSE.txt',
        'futurize.py',
        'pasteurize.py',
        'discover_tests.py',
        'check_rst.sh',
        'TESTING.txt',
    ],
    'tests': ['*.py'],
}

REQUIRES = []
TEST_REQUIRES = []
if sys.version_info[:2] == (2, 6):
    REQUIRES += ['importlib', 'argparse']
    TEST_REQUIRES += ['unittest2']

import src.future
VERSION = src.future.__version__
DESCRIPTION = "Clean single-source support for Python 3 and 2"
LONG_DESC = src.future.__doc__
AUTHOR = "Ed Schofield"
AUTHOR_EMAIL = "ed@pythoncharmers.com"
URL = "https://python-future.org"
LICENSE = "MIT"
KEYWORDS = "future past python3 migration futurize backport six 2to3 modernize pasteurize 3to2"
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
]

setup_kwds = {}

try:
    SYSTEM_MODULES = set([
        '_dummy_thread',
        '_markupbase',
        '_thread',
        'builtins',
        'configparser',
        'copyreg',
        'html',
        'http',
        'queue',
        'reprlib',
        'socketserver',
        'tkinter',
        'winreg',
        'xmlrpc'
    ])

    if sys.version_info[0] >= 3:
        files = os.listdir(os.path.join('build', 'lib'))
        if len(set(files) & set(SYSTEM_MODULES)) > 0:
            print('ERROR: Your build folder is in an inconsistent state for '
                  'a Python 3.x install. Please remove it manually and run '
                  'setup.py again.', file=sys.stderr)
            sys.exit(1)
except OSError:
    pass

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    license=LICENSE,
    keywords=KEYWORDS,
    entry_points={
        'console_scripts': [
            'futurize = libfuturize.main:main',
            'pasteurize = libpasteurize.main:main'
        ]
    },
    package_dir={'': 'src'},
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIRES,
    classifiers=CLASSIFIERS,
    test_suite="discover_tests",
    tests_require=TEST_REQUIRES,
    **setup_kwds
)
