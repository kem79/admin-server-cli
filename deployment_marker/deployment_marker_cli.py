import click
import requests

from configuration.configuration import Configuration
from common.utils import print_response, protocol


@click.group()
def cli():
    """
    Simple CLI to list, create and delete deployment markers in New Relic through RailAi admin server interactions
    """
    pass


@cli.command(name='list', help='List deployment markers for NAME')
@click.argument('name')
def list_deployment_markers(name):
    """
    List deployment markers for NAME.
    \f
    :param name: the name of the micro-service
    :return: print response
    """
    url = '{}://{}/api/v1/{}/deployment-marker'.format(protocol(),
                                                       Configuration().get('url'),
                                                       name)
    resp = requests.get(url)
    print_response(resp)


@cli.command(name='create', help='Create deployment marker for NAME')
@click.argument('name')
@click.argument('version')
@click.option('--commit', help='The commit id', default='N/A')
@click.option('--changelog', help='The change log', default='N/A')
@click.option('--description', help='The description of the change', default='N/A')
@click.option('--username', help='The committer name', default='N/A')
def create_deployment_marker(name, version, commit, changelog, description, username):
    """
    Create deployment marker for NAME
    \f
    :param name: the name of the micro-service
    :param version: the version of the micro-service
    :param commit: the id of the commit
    :param changelog: the change log information
    :param description: the description
    :param username: the user name
    :return: print response
    """
    url = '{}://{}/api/v1/{}/deployment-marker'.format(protocol(),
                                                       Configuration().get('url'),
                                                       name)
    resp = requests.post(url=url,
                         headers={'content-type': 'application/json'},
                         json={"version": version,
                               "commit": commit,
                               "changelog": changelog,
                               "description": description,
                               "username": username})
    print_response(resp)


@cli.command('delete', help='Delete deployment marker ID for NAME')
@click.argument('name')
@click.argument('deployment_id')
def delete_deployment_marker(name, deployment_id):
    """
    Delete deployment marker ID for NAME
    :param name: the name of the micro-service
    :param deployment_id: the id of the deployment marker
    :return: print response
    """
    url = '{protocol}://{url}/api/v1/{name}/deployment-marker/{deployment_id}'.format(
        protocol=protocol(),
        url=Configuration().get('url'),
        name=name,
        deployment_id=deployment_id
    )
    resp = requests.delete(url=url)
    print_response(resp)

