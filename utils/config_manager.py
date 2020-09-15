import yaml
import os
import logging

# Init logger.
logger = logging.getLogger('CoreDump')

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../config.yml')


class ConfigManager():

    def __init__(self):

        try:
            with open(CONFIG_FILE_PATH, 'r') as cfg_file:
                self.cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            logger.error('Could not find config file!')

    def get_command_prefix(self):

        return self.cfg['bot_settings']['command_prefix']

    def get_presence(self):

        return self.cfg['bot_settings']['presence']
