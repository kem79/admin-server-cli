import json

import click
import requests


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
    url = 'https://' \
          'api/v1/{}/deployment-marker'.format(name)
    resp = requests.get(url=url)
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
    url = 'https://admin-server.cfd.isus.emc.com/api/v1/{}/deployment-marker'.format(name)
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
    url = 'https://admin-server.cfd.isus.emc.com/api/v1/{name}/deployment-marker/{deployment_id}'.format(
        **locals())
    resp = requests.delete(url=url)
    print_response(resp)


def with_color(status_code):
    """
    Define the color of the message
    :return: a string representing the color
    """
    if status_code in range(200, 299):
        return 'green'
    elif status_code in range(400, 499):
        return 'yellow'
    else:
        return 'red'


def print_response(resp):
    """
    Print the
    :param resp:
    :return:
    """
    click.secho('\n'.join([str(resp.status_code),
                           json.dumps(resp.json(), indent=2),
                           ]),
                fg=with_color(resp.status_code))



if __name__ == "__main__":
    cli()
