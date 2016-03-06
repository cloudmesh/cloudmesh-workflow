from setuptools import setup, find_packages
from setup_util import write_version_module

VERSION = '0.1.2'

write_version_module(VERSION, 'cloudmesh_workflow/version.py')

requirements = [
    'pydotplus',
    'networkx',
    'futures',
    'astor',
    'traits'
]


setup(
    name='cloudmesh_workflow',
    version=VERSION,
    packages=find_packages(),
    license='Apache 2.0',
    install_requires=requirements,
)
