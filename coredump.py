import logging


import discord
from discord.ext import commands

COMMAND_PREFIX = '!'
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

    def __init__(self):
        self.token = load_token()
        super().__init__(command_prefix=COMMAND_PREFIX)

        self.load_extension('extensions.test_commands')

    def get_token(self):
        return self.token

    async def on_ready(self):
        logger.info('Logged in as {}.'.format(self.user))

        logger.info('Changing bot presence...')
        await self.change_presence(activity=discord.Game(name='Disfrutando el cambio de horarios.'))

    async def on_message(self, message):
        await self.process_commands(message)


def main():

    coredump = CoreDump()
    coredump.run(coredump.get_token())


if __name__ == '__main__':
    main()
