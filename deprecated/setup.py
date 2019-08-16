from setuptools import setup, find_packages
from setup_util import write_version_module

VERSION = '0.1.2'

write_version_module(VERSION, 'cloudmesh.workflow/version.py')

setup(
    name='cloudmesh.workflow',
    version=VERSION,
    packages=find_packages(),
    license='Apache 2.0',
)
