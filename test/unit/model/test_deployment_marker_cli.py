import os

import yaml
from doublex import assert_that, is_
from nose2.tools import such
from click.testing import CliRunner

from railai_admin_server_cli.config_cli import config_admin_server_url, print_config
from railai_admin_server_cli.model.configuration import Configuration

with such.A("Deployment Marker CLI") as it:
    @it.has_setup
    def setup():
        it.runner = CliRunner()

    with it.having('there is no configuration file'):
        @it.has_setup
        def setup():
            if os.path.exists(it.configuration.config_file_path):
                os.remove(it.configuration.config_file_path)