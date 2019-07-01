import click
import requests

from common.utils import print_response, poll_task_result, protocol
from configuration.configuration import Configuration

headers = {'accept': 'application/json'}

@click.group()
def cli():
    """
    Simple CLI to create, get, delete performance baseline.
    """
    pass


@cli.command(name='get')
@click.argument('name')
@click.argument('number_of_users')
@click.argument('hatch_rate', default='10')
def get_performance_baseline(name, number_of_users, hatch_rate):
    """Get performance baseline for NAME.

    ex: aspb get data-metrics-api-performance 10 5

    \b
    This command returns the performance baseline of data-metrics-api-performance for 10 concurrent users and a hatch
    rate of 5 users per seconds.
    Notice that the name of the application is the name of the application registered in New Relic.

    \b
    :param name: the name of the micro-service
    :param number_of_users: the number of users
    :param hatch_rate: the hatch rate of users
    :return: print response
    """
    url = '{}://{}/api/v1/performance-baselines/{}?number_of_users={}&hatch_rate={}'.format(
        protocol(),
        Configuration().get('url'),
        name,
        number_of_users,
        hatch_rate
    )
    resp = requests.get(url,
                        headers=headers)
    print_response(poll_task_result(resp.json()['data']))


@cli.command(name='all')
@click.argument('name')
def get_all_performance_baselines(name):
    """Get all performance baselines for NAME.

    ex: aspb all data-metrics-service-performance

    \b
    :param name: the name of the micro-service
    :return: print response
    """
    url = '{}://{}/api/v1/performance-baselines/{}'.format(
        protocol(),
        Configuration().get('url'),
        name
    )
    resp = requests.get(url,
                        headers=headers)
    print_response(poll_task_result(resp.json()['data']))


@cli.command(name='delete')
@click.argument('name')
@click.argument('number_of_users')
@click.argument('hatch_rate')
def delete_performance_baseline(name, number_of_users, hatch_rate):
    """Delete performance baseline for NAME.

    ex: aspb delete data-metrics-service-performance 10 1

    This command deletes the performance baseline of data-metrics-service-performance for 10 concurrent user and a
    hatch rate of 1 user per second.

    \b
    :param name: the name of the micro-service
    :param number_of_users: the number of users
    :param hatch_rate: the hatch rate of users
    :return: print response
    """
    url = '{}://{}/api/v1/performance-baselines/{}'.format(
        protocol(),
        Configuration().get('url'),
        name,
    )
    resp = requests.delete(url,
                           json={"number_of_users": number_of_users,
                                 "hatch_rate": hatch_rate},
                           headers=headers)
    print_response(resp)


@cli.command(name='create')
@click.argument('name')
@click.argument('url')
@click.argument('number_of_users')
@click.argument('hatch_rate')
@click.argument('locustfile')
@click.option('-d', '--duration', default=3600)
def create_performance_baseline(name, url, number_of_users, hatch_rate, duration, locustfile):
    """Create performance baseline for NAME.
    ex: aspb create data-metrics-api-performance data-metrics-api-perf.cfd.isus.emc.com 10 2 locustfile_data_metrics_api.py

    \b
    This command creates a baseline for data-metrics-api-perf deployed with route
    data-metrics-api-perf.cfd.isus.emc.com with 10 concurrent users with a user hatch rate of 2.
    The duration will be set to 3600 seconds by default

    \b
    :param name: the name of the micro-service
    :param url: the url to the application under test
    :param number_of_users: the number of users
    :param hatch_rate: the hatch rate of users
    :param locustfile: the name of the locust file
    :param duration: the duration of the performance baseline
    :return: print response
    """
    create_baseline_url = '{}://{}/api/v1/performance-baselines'.format(
        protocol(),
        Configuration().get('url')
    )
    locust_file_name = locustfile if locustfile else 'locust_{}.py'.format(name.replace('-', '_'))
    resp = requests.post(create_baseline_url,
                         json={"name": name,
                               "url": url,
                               "number_of_users": number_of_users,
                               "hatch_rate": hatch_rate,
                               "locust_file": locust_file_name,
                               "duration": duration},
                         headers=headers)
    click.secho('Create performance baseline for {}, {} concurrent users with locust file {}'
                ' ({} users hatch rate, {} seconds)'.format(name,
                                                            number_of_users,
                                                            locust_file_name,
                                                            hatch_rate,
                                                            duration),
                fg='green' if resp.status_code == 200 else 'red')
    print_response(resp)
