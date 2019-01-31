import os

import yaml
from doublex import assert_that, is_
from hamcrest import has_key, raises, calling, contains_string
from nose2.tools import such
from pathlib import Path
from railai_admin_server_cli.model.configuration import Configuration

with such.A("Configuration") as it:
    @it.has_setup
    def setup():
        it.config_file_path = os.path.join(str(Path.home()), '.railai-admin-server-test.yml')
        it.config = Configuration(it.config_file_path)


    with it.having('no configuration is setup'):
        @it.has_setup
        def setup():
            if os.path.exists(it.config_file_path):
                os.remove(it.config_file_path)

        with it.having('add(key, value)'):
            @it.has_setup
            def setup():
                it.config.add('url', 'admin-server.cfd.isus.emc.com')
                with open(it.config_file_path, 'r') as f:
                    it.content = yaml.load(f)

            @it.should('create the configuration file')
            def test_config_file_created():
                assert_that(os.path.isfile(it.config_file_path), is_(True))

            @it.should('add a key/value pair to the configuration file.')
            def test_add():
                assert_that(it.content, has_key('url'))
                assert_that(it.content['url'], is_('admin-server.cfd.isus.emc.com'))

            @it.has_teardown
            def teardown():
                os.remove(it.config_file_path)

        with it.having('get(key)'):

            @it.should('raise a FileNotFound exception.')
            def test_raise_error_when_conf_file_not_present():
                assert_that(calling(it.config.get).with_args('url'),
                            raises(FileNotFoundError,
                                   'The configuration could not be found. Create your configuration with asconf CLI.'))

    with it.having('a configuration file already exists with key \'url\''):
        @it.has_setup
        def setup():
            if os.path.exists(it.config_file_path):
                os.remove(it.config_file_path)
            it.config.add('url', 'admin-server.cfd.isus.emc.com')

        with it.having('i had a new key \'bar\''):
            @it.has_setup
            def setup():
                it.config.add('bar', 'foo')
                with open(it.config_file_path, 'r') as f:
                    it.content = yaml.safe_load(f)

            @it.should('append the key to the config file.')
            def test_append_new_key():
                assert_that(it.content['bar'], is_('foo'))

            @it.should('not affect the existing key \'url\'')
            def test_url_key_is_unaffected():
                assert_that(it.content['url'], is_('admin-server.cfd.isus.emc.com'))

        with it.having('get(key) on an existing key'):

            @it.should('return the key value')
            def test_get_existing_key():
                assert_that(it.config.get('url'), is_('admin-server.cfd.isus.emc.com'))

        with it.having('get(key) on an non existing key'):

            @it.should('return a KeyError exception.')
            def test_get_existing_key():
                assert_that(calling(it.config.get).with_args('unknown'),
                            raises(KeyError,
                                   'The key is not defined. Create it first with asconf unknown VALUE.'))

        @it.has_teardown
        def teardown():
            os.remove(it.config_file_path)


it.createTests(globals())

if __name__ == "__main__":
    import nose2
    nose2.main()
