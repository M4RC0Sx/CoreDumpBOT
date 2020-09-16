import yaml
import os
import logging

# Init logger.
logger = logging.getLogger('CoreDump')

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../config.yml')
IMG_DIR_PATH = os.path.join(os.path.dirname(__file__), '../media/img/')


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

    def get_crypto_channel(self):

        return int(self.cfg['bot_settings']['channel_ids']['crypto_channel'])

    def get_verification_channel(self):

        return int(self.cfg['bot_settings']['channel_ids']['verification_channel'])

    def get_welcome_channel(self):

        return int(self.cfg['bot_settings']['channel_ids']['welcome_channel'])

    def get_verified_role(self):

        return int(self.cfg['bot_settings']['role_ids']['verified_role'])

    def get_developer_role(self):

        return int(self.cfg['bot_settings']['role_ids']['developer_role'])

    def get_verification_emoji(self):

        return self.cfg['bot_settings']['emoji_ids']['verification_emoji']

    def get_noperms_msg(self):

        return self.cfg['bot_settings']['messages']['noperms_msg']

    def get_img_dir(self):

        return IMG_DIR_PATH
