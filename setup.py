from setuptools import setup

setup(
    name="railai-admin-server-cli",
    version="0.0.1",
    author="Marc",
    author_email="marc.marechal@emc.com",
    description="a simple CLI to interact with railai admin server.",
    packages=['railai_admin_server_cli'],
    install_requires=[
        'click',
        'requests',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'asdm =     railai_admin_server_cli.deployment_marker_cli:cli',
            'asconf =   railai_admin_server_cli.config_cli:cli'
        ]}
)