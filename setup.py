#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="golem",
    version="0.0.1",
    author='Adam Victor Brandizzi',
    author_email='adam@brandizzi.com.br',
    description='It is alive!* **',
    long_description="""
    It is alive!* **

    * "it" == one HTML document.
    ** outside a browser!
    """,
    license='LGPLv3',
    url='http://bitbucket.com/brandizzi/golem',

    packages=find_packages(),
    test_suite='golem.test',
    test_loader='unittest:TestLoader',
    tests_require=['requests', 'inelegant']
)
