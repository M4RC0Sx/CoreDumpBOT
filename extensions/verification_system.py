import logging


from discord.ext import commands

from utils.config_manager import ConfigManager


# Init logger.
logger = logging.getLogger('CoreDump')


# Load config manager.
cm = ConfigManager()


class VerificationSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.unverified_users = []

    @commands.command(name='verificationmsg')
    @commands.has_role(cm.get_developer_role())
    async def _cmd_verification_msg(self, ctx):

        verification_channel_id = cm.get_verification_channel()
        channel_id = ctx.channel.id

        if verification_channel_id == channel_id:

            msg = await ctx.channel.send("Mensaje de verificación.")
            await msg.add_reaction(cm.get_verification_emoji())

    @commands.Cog.listener()
    async def on_member_join(self, member):

        self.unverified_users.append(member.id)

    @commands.Cog.listener()
    async def on_member_leave(self, member):

        member_id = member.id

        if member_id in self.unverified_users:
            logger.info(
                'A member with ID {} has left without verification. Removing him from cache...'.format(member_id))
            self.unverified_users.remove(member_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        channel_id = payload.channel_id
        verification_channel_id = cm.get_verification_channel()

        if channel_id == verification_channel_id:

            member = payload.member

            # Ignore reactions added by the bot.
            if member == self.bot.user:
                return

            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(channel_id)
            emoji = self.bot.get_emoji(payload.emoji.id)
            message = await channel.fetch_message(payload.message_id)

            verified_role_id = cm.get_verified_role()
            verified_role = guild.get_role(verified_role_id)

            # If member not in unverified cache, remove reaction.
            if member.id not in self.unverified_users or member.has_role(verified_role_id):
                await message.remove_reaction(emoji, member)
                return

            await member.add_roles([verified_role, ])
            self.unverified_users.remove(member.id)


def setup(bot):
    bot.add_cog(VerificationSystem(bot))
    logger.info("Extension loaded: verification_system")
