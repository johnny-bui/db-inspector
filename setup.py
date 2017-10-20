# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

setup(
    name='db-inspector',
    version='0.1.0',
    description='A tool to inspect schema in relational Database',
    long_description=readme,
    author='lazyboy',
    author_email='noemail@noemail',
    keywords='database datavisual',
    python_requires='>=3',
    url='',
    license=_license,
    packages=find_packages(
        exclude=('tests', 'docs')
    ),
    install_requires=['PyYAML', 'sqlalchemy', 'Psycopg2'],
    entry_points={
        'console_script': [
            'db-inspector = dbinspector.main:main'
        ]
    }
)
