import click
from railai_admin_server_cli.model.configuration import Configuration

@click.group()
def cli():
    """
    Simple CLI to configure your admin server client
    :return:
    """
    pass


@cli.command(name='url', help='Configure the URL of admin server.')
@click.argument('url')
def config_admin_server_url(url):
    """
    Create an environment variable to hold the admin server url.
    :param url: the url to admin server, ex: admin-server.cfd.isus.emc.com/
    :return: None
    """
    Configuration().add('url', url)
    click.secho('Added url: {} to configuration file.'.format(url))


@cli.command(name='list', help='Print the configuration.')
def print_config():
    """
    Print the configuration of the CLI to the screen
    :return:
    """
    click.secho(Configuration().list())
