import logging
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks

from utils import crypto_api

from utils.config_manager import ConfigManager


# Init logger.
logger = logging.getLogger('CoreDump')


# Load config manager.
cm = ConfigManager()


class CryptoBroadcasts(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.broadcast_crypto.start()

    @tasks.loop(hours=1.0)
    async def broadcast_crypto(self):

        data = crypto_api.get_crypto_prices()

        format_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        embed_msg = discord.Embed(
            title='Precios de Criptomonedas', description=' ', color=0x00ff00)
        embed_msg.set_author(
            name='CoreDump', icon_url=self.bot.user.avatar_url)

        for crypto in data.keys():
            embed_msg.add_field(name=crypto.upper(), value='{}$ / {}€'.format(
                data[crypto]['usd'], data[crypto]['eur']), inline=False)

        embed_msg.set_footer(
            text='CoreDump [{}]'.format(format_date), icon_url=self.bot.user.avatar_url)
        embed_msg.set_thumbnail(url=self.bot.user.avatar_url)

        await self.bot.get_channel(cm.get_crypto_channel()).send(embed=embed_msg)
        logger.info('Cryptocurrency broadcast published!')


def setup(bot):
    bot.add_cog(CryptoBroadcasts(bot))
    logger.info("Extension loaded: crypto_broadcasts")
