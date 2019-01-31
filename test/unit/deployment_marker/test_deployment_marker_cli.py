import os

import responses
from doublex import assert_that
from hamcrest import contains_string
from nose2.tools import such
from click.testing import CliRunner

from deployment_marker.deployment_marker_cli import list_deployment_markers
from deployment_marker.deployment_marker_cli import create_deployment_marker
from deployment_marker.deployment_marker_cli import delete_deployment_marker
from configuration.configuration import Configuration

with such.A("Deployment Marker CLI") as it:
    @it.has_setup
    def setup():
        it.runner = CliRunner()
        it.config = Configuration()

    with it.having('there is a configuration file setup with \'url\' defined'):
        @it.has_setup
        def setup():
            if os.path.exists(it.config.config_file_path):
                os.remove(it.config.config_file_path)
            it.config.add('url', 'example.com')

        with it.having('list deployment markers'):
            @it.has_setup
            @responses.activate
            def setup():
                responses.add(responses.GET,
                              'https://example.com/api/v1/data-storage-mongo/deployment-marker',
                              json={"data": {"deployments": []}, "message": "", "status": ""},
                              status=200
                              )
                it.result = it.runner.invoke(list_deployment_markers, ['data-storage-mongo'])

            @it.should('print the response status code to the screen')
            def test_list_print_status_code():
                assert_that(it.result.output, contains_string('200'))

            @it.should('print the response message to the screen')
            def test_list_print_response_message():
                assert_that(it.result.output, contains_string('deployments'))

        with it.having('create deployment marker'):
            @it.has_setup
            @responses.activate
            def setup():
                responses.add(responses.POST,
                              'https://example.com/api/v1/data-storage-mongo/deployment-marker',
                              json={"data": {"id": 1234}, "message": "", "status": ""},
                              status=201
                              )
                it.result = it.runner.invoke(create_deployment_marker, ['data-storage-mongo',
                                                                        '1.0.1244325'])

            @it.should('print the response status code to the screen')
            def test_create_print_status_code():
                assert_that(it.result.output, contains_string('201'))

            @it.should('print the response message to the screen')
            def test_create_print_response_message():
                assert_that(it.result.output, contains_string('1234'))

        with it.having('delete deployment marker'):
            @it.has_setup
            @responses.activate
            def setup():
                responses.add(responses.DELETE,
                              'https://example.com/api/v1/data-storage-mongo/deployment-marker/987',
                              json={"data": {"deployment": {"id": 987}}, "message": "", "status": ""},
                              status=200
                              )
                it.result = it.runner.invoke(delete_deployment_marker, ['data-storage-mongo',
                                                                        '987'])

            @it.should('print the response status code to the screen')
            def test_create_print_status_code():
                assert_that(it.result.output, contains_string('200'))

            @it.should('print the response message to the screen')
            def test_create_print_response_message():
                assert_that(it.result.output, contains_string('987'))

it.createTests(globals())