from setuptools import setup, find_packages
import os

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name="railai-admin-server-cli",
    version="0.0.1",
    author="Marc",
    author_email="marc.marechal@emc.com",
    description="a simple CLI to interact with railai admin server.",
    long_description=read('README.md'),
    url='http://10.62.81.24/incubation/railai-admin-server-cli',
    packages=['configuration',
              'deployment_marker'],
    install_requires=[
        'click==6.7',
        'requests==2.18.4',
        'colorama==0.4.1',
        'pyyaml==3.13'
    ],
    python_requires=">3",
    entry_points={
        'console_scripts': [
            'asdm =     deployment_marker.deployment_marker_cli:cli',
            'asconf =   configuration.config_cli:cli'
        ]}
)