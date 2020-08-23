#!/usr/bin/env python

# Copyright (c) 2020, Pureport, Inc
# All Rights Reserved.

import os

from setuptools import setup
from setuptools import find_packages

from pureport_client import __version__
from pureport_client import __author__


def main():
    base_path = os.path.dirname(__file__)

    with open(os.path.join(base_path, 'README.md')) as f:
        long_description = f.read()

    with open(os.path.join(base_path, 'requirements.txt')) as f:
        requirements = f.readlines()


    setup(
        name="pureport-client",
        version=__version__,
        description="Pureport client command line interface",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Environment :: Web Environment",
            "intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Internet",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Software Development :: Libraries",
        ],
        keywords="pureport multicloud fabric network cloud automation",
        author=__author__,
        author_email="info@pureport.com",
        url="https://www.pureport.com",
        project_urls={
            "Documentation": "https://pureport-client.readthedocs.io",
            "Code": "https://github.com/pureport/pureport-python-client",
            "Issue tracker": "https://github.com/pureport/pureport-python-client/issues"
        },
        license="MIT",
        packages=find_packages(),
        install_requires=requirements,
        include_package_data=True,
        python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
        entry_points={
            'console_scripts': [
                'pureport=pureport_client.__main__:run'
            ]
        },
    )

if __name__ == '__main__':
    main()
