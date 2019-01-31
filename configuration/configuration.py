import os
import yaml
from pathlib import Path


class Configuration:

    def __init__(self,
                 config_file_path=os.path.join(str(Path.home()),
                                               os.getenv('ADMIN_SERVER_CONFIG_FILE_PATH', '.railai-admin-server.yml'))
                 ):
        self.config_file_path = config_file_path

    def list(self):
        """
        return the configuration
        :return:
        """
        try:
            with open(self.config_file_path, 'r') as f:
                return yaml.dump(yaml.load(f), default_flow_style=False)
        except FileNotFoundError:
            return 'No configuration file detected. Create your configuration first.'

    def add(self, key, value):
        """
        add a key/value pair to the config
        :param key:
        :param value:
        :return:
        """
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r+') as f:
                data_dict = yaml.load(f)
                data_dict[key] = value
            with open(self.config_file_path, 'w') as f:
                yaml.dump(data_dict, f, default_flow_style=False)
        else:
            with open(self.config_file_path, 'w+') as f:
                f.write('{}: {}'.format(key, value))

    def get(self, key):
        """
        Return a key value from the configuration file.
        :param key:
        :return:
        """
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r+') as f:
                data_dict = yaml.load(f)
                try:
                    return data_dict[key]
                except KeyError:
                    raise KeyError('The key is not defined. Create it first with asconf {} VALUE.'.format(key))
        else:
            raise FileNotFoundError('The configuration could not be found. Create your configuration with asconf CLI.')
