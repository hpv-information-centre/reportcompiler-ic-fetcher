""" Module for installing module as pip package """
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(
    os.path.normpath(
        os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='reportcompiler-ic-fetcher',
    version='0.3.0',
    packages=find_packages('.'),
    include_package_data=True,
    license='MIT License',
    description='Report Compiler Information Centre fetcher is a plugin for '
                'the Report Compiler library that extends the MySQL fetcher '
                'to support sources, notes and other info related to the '
                'fetched data. The plugin expects a particular database '
                'structure and it will be used in the HPV Information Centre '
                'project.',
    long_description=README,
    url='https://www.hpvcentre.net',
    author='David Gómez',
    author_email='info@hpvcenter.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'reportcompiler',
        'pymysql',
    ],
    entry_points={
        'reportcompiler.data_fetchers': [
            'mysql_ic=reportcompiler_ic_fetcher.mysql_ic:MySQLICFetcher',
        ],
    }
)
