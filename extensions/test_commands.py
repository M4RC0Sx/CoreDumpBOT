import logging


from discord.ext import commands

# Init logger.
logger = logging.getLogger('CoreDump')


class TestCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def _cmd_test(self, ctx):
        await ctx.channel.send("¡Funcionando {}!".format(ctx.author.mention))


def setup(bot):
    bot.add_cog(TestCommands(bot))
    logger.info("Extension loaded: test_commands")
