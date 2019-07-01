from setuptools import setup, find_packages
import json


with open('material.json', 'r') as f:
    data = json.load(f)
    package_name = data['package_name'].strip()
    version = data['version'].strip()
    long_description = data['long_description'].strip()

setup(
    name=package_name,
    version=version,
    author="Marc",
    author_email="marc.marechal@emc.com",
    description="a simple CLI to interact with railai admin server.",
    long_description=long_description,
    url='http://10.62.81.24/incubation/railai-admin-server-cli',
    packages=find_packages(),
    install_requires=[
        'click==6.7',
        'requests==2.18.4',
        'colorama==0.4.1',
        'pyyaml==3.13'
    ],
    python_requires=">=3",
    entry_points={
        'console_scripts': [
            'asdm =     deployment_marker.deployment_marker_cli:cli',
            'asconf =   configuration.config_cli:cli',
            'aspb =     performance_baseline.performance_baseline_cli:cli',
            'aspbr =    performance_baseline.performance_baseline_report_cli:cli'
        ]}
)