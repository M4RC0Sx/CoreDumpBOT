import logging


from discord.ext import commands

from utils.config_manager import ConfigManager

# Init logger.
logger = logging.getLogger('CoreDump')


# Load config manager.
cm = ConfigManager()


class UtilityCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clean')
    @commands.has_role(cm.get_admin_role())
    async def _cmd_clean(self, ctx, qty: int):

        if not qty or qty <= 0:
            raise commands.BadArgument

        with ctx.channel.typing():
            msgs = await ctx.channel.history(limit=qty).flatten()
            await ctx.channel.delete_messages(msgs)

        await ctx.send("**LIMPIEZA >>** ¡Has borrado {} mensajes correctamente! {}".format(len(msgs), ctx.author.mention))

    @_cmd_clean.error
    async def _cmd_clean_error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await ctx.send("**ERROR >>** ¡Debes especificar un entero mayor que 0! {}".format(ctx.author.mention))

        elif isinstance(error, commands.MissingRole):
            await ctx.send("{} {}".format(cm.get_noperms_msg(), ctx.author.mention))


def setup(bot):
    bot.add_cog(UtilityCommands(bot))
    logger.info("Extension loaded: utility_commands")
