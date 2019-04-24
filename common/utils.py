import os

import click
import json

from time import sleep

import requests

from configuration.configuration import Configuration


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


def poll_task_result(task_id, polling_interval=100):
    get_task_result_url = 'http://{}/api/v1/tasks/{}'.format(Configuration().get('url'),
                                                             task_id)
    while True:
        resp = requests.get(get_task_result_url)
        if resp.json()['status'] != 'PENDING':
            break
        sleep(polling_interval)
    return resp


def protocol():
    conf = Configuration()
    if conf.get('url').find('localhost') > -1:
        return 'http'
    return 'https'
