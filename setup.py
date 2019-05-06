# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pureport-client',
    version='0.0.5',
    author='Pureport',
    author_email='noreply@pureport.com',
    license='MIT',
    description='An API client for the Pureport ReST API',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pureport/pureport-python-client',
    packages=find_packages(),
    namespace_packages=[
        'pureport',
        'pureport.api',
        'pureport.exception',
        'pureport.util'
    ],
    install_requires=[
        'requests',
        'enum34'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ]
)
