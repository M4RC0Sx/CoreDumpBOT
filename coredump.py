import logging

import discord
from discord.ext import commands

from utils.config_manager import ConfigManager


TOKEN_FILE = '.token'


# Init and config logger.
logger_level = logging.INFO
logger_format = '[%(levelname)s/%(asctime)s] %(message)s'
logger_handlers = [logging.FileHandler(
    'coredump.log'), logging.StreamHandler()]

logging.basicConfig(
    format=logger_format, level=logger_level, handlers=logger_handlers)
logger = logging.getLogger('CoreDump')


def load_token():

    # Read token from file.
    with open(TOKEN_FILE, 'r') as tf:
        token = tf.read()

    return token


class CoreDump(commands.Bot):

    def __init__(self, config_manager):

        self.cm = config_manager

        self.token = load_token()
        super().__init__(command_prefix=self.cm.get_command_prefix())

    def get_token(self):
        return self.token

    def load_extensions(self):

        self.load_extension('extensions.test_commands')
        self.load_extension('extensions.crypto_broadcasts')

    async def on_ready(self):

        logger.info('Logged in as {}.'.format(self.user))

        self.load_extensions()

        logger.info('Changing bot presence...')
        await self.change_presence(activity=discord.Game(name=self.cm.get_presence()))

    async def on_message(self, message):

        await self.process_commands(message)


def main():

    cm = ConfigManager()

    coredump = CoreDump(cm)
    coredump.run(coredump.get_token())


if __name__ == '__main__':
    main()
