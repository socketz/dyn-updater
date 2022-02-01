# -*- coding: utf-8 -*-

__version__ = '0.1.1'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name="dyn-updater",
    version=__version__,
    author="socketz",
    author_email='info@socketz.net',
    description="Python automated DynHost updater using OVH API",
    long_description=readme,
    license="http://creativecommons.org/licenses/by-sa/3.0/",
    url="https://github.com/socketz/dyn-updater",
    platforms=["any"],
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: Attribution Assurance License",
        'Intended Audience :: Developers',
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 1 - Beta',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
