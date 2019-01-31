import os

import yaml
from doublex import assert_that, is_
from nose2.tools import such
from click.testing import CliRunner

from configuration.config_cli import config_admin_server_url, print_config
from configuration.configuration import Configuration

with such.A("asconf CLI") as it:
    @it.has_setup
    def setup():
        it.runner = CliRunner()
        it.configuration = Configuration()

    with it.having('there is no configuration file'):
        @it.has_setup
        def setup():
            if os.path.exists(it.configuration.config_file_path):
                os.remove(it.configuration.config_file_path)

        with it.having('i invoke url command with NAME admin-server.cfd.isus.emc.com'):
            @it.has_setup
            def setup():
                it.result = it.runner.invoke(config_admin_server_url, ['admin-server.cfd.isus.emc.com'])

            @it.should('succeed')
            def test_succeed():
                assert_that(it.result.exit_code, is_(0))

            @it.should('print \'Added url: admin-server.cfd.isus.emc.com to configuration file.\'')
            def test_url_success_message():
                assert_that(it.result.output, is_('Added url: admin-server.cfd.isus.emc.com to configuration file.\n'))

        @it.has_teardown
        def teardown():
            if os.path.exists(it.configuration.config_file_path):
                os.remove(it.configuration.config_file_path)

    with it.having('there is already a configuration file with key \'url\' defined'):
        @it.has_setup
        def setup():
            it.configuration.add('url', 'admin-server.cfd.isus.emc.com')

        @it.should('update \'url\' if i assigned it a new value')
        def test_key_updated():
            it.result = it.runner.invoke(config_admin_server_url, ['bar'])
            with open(it.configuration.config_file_path, 'r') as f:
                assert_that(yaml.load(f)['url'], is_('bar'))

        @it.has_teardown
        def teardown():
            os.remove(it.configuration.config_file_path)

    with it.having('there is no configuration file setup'):
        @it.has_setup
        def setup():
            if os.path.exists(it.configuration.config_file_path):
                os.remove(it.configuration.config_file_path)

        with it.having('i invoke the list command'):
            @it.has_setup
            def setup():
                it.result = it.runner.invoke(print_config)

            @it.should('return \'No configuration file detected. Create your configuration first.\'')
            def test_error_message_when_config_file_is_missing():
                assert_that(it.result.output, is_('No configuration file detected. Create your configuration first.\n'))

    with it.having('there is a configuration file setup'):
        @it.has_setup
        def setup():
            it.configuration.add('url', 'admin-server.cfd.isus.emc.com')
            it.configuration.add('foo', 'bar')

        with it.having('i invoke the list command'):
            @it.has_setup
            def setup():
                it.result = it.runner.invoke(print_config)

            @it.should('print the configuration')
            def test_print_configuration():
                assert_that(it.result.output, is_('foo: bar\nurl: admin-server.cfd.isus.emc.com\n\n'))


    @it.has_teardown
    def teardown():
        if os.path.exists(it.configuration.config_file_path):
            os.remove(it.configuration.config_file_path)

it.createTests(globals())

if __name__ == "__main__":
    import nose2
    nose2.main()
