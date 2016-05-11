from setuptools import setup, find_packages
from setup_util import write_version_module


VERSION = '1.0'

write_version_module(VERSION, 'cloudmesh_workflow/version.py')

setup(
    name='workflow',
    version=VERSION,
    packages=find_packages(),
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'cm-w = cloudmesh_workflow.wrapper:main',
        ],
    },
)
