# -*- coding: utf-8 -*-
from setuptools import setup, find_namespace_packages


def read_file(file_name):
    """Read file and return its contents."""
    with open(file_name, 'r') as f:
        return f.read()


def read_requirements(file_name):
    """Read requirements file as a list."""
    reqs = read_file(file_name).splitlines()
    if not reqs:
        raise RuntimeError(
            "Unable to read requirements from the %s file"
            % file_name
        )
    return reqs


setup(
    name='pureport-client',
    version='1.0.11',
    author='Pureport',
    author_email='noreply@pureport.com',
    license='MIT',
    description='An API client for the Pureport ReST API',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pureport/pureport-python-client',
    packages=find_namespace_packages(include=[
        'pureport.*',
        'pureport.api.*',
        'pureport.cli.*',
        'pureport.exception.*',
        'pureport.util.*'
    ]),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'pureport=pureport.cli.cli:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
