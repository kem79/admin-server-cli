import click
import requests

from common.utils import print_response, poll_task_result, protocol
from configuration.configuration import Configuration


@click.group()
def cli():
    """
    Simple CLI to create performance baseline report for a given application.
    """
    pass


@cli.command(name='create')
@click.argument('name')
def create_performance_baseline_report(name):
    """Create performance baseline report for NAME.

    ex: aspbr create data-metrics-api-performance

    \b
    Long description here.

    \b
    :param name: the name of the micro-service
    :return: print response
    """
    url = '{}://{}/api/v1/performance-baseline-reports'.format(
        protocol(),
        Configuration().get('url')
    )
    resp = requests.post(url,
                         json={"application_name": name},
                         headers={'accept': 'application/json'})
    print_response(resp)