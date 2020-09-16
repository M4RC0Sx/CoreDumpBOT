import logging
import io
from PIL import Image, ImageDraw, ImageFont


from discord import File
from discord.ext import commands

from utils.config_manager import ConfigManager
from utils.custom_exceptions import ForbiddenChannelException


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

            msg = await ctx.channel.send('Mensaje de verificación.')
            await msg.add_reaction(cm.get_verification_emoji())

        else:

            raise ForbiddenChannelException

    @_cmd_verification_msg.error
    async def _cmd_verification_msg_error(self, ctx, error):

        if isinstance(error, ForbiddenChannelException):
            await ctx.send("{} {}".format(cm.get_forbiddenchannel_msg(), ctx.author.mention))

        elif isinstance(error, commands.MissingRole):
            await ctx.send("{} {}".format(cm.get_noperms_msg(), ctx.author.mention))

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
            # TODO Check if member has verified role? Must make a Role object loop.
            # if member.id not in self.unverified_users or member.has_role(verified_role_id):
            if member.id not in self.unverified_users:
                await message.remove_reaction(emoji, member)
                return

            # Add verified role, remove user from cache and remove user reaction.
            await member.add_roles(verified_role)
            self.unverified_users.remove(member.id)
            await message.remove_reaction(emoji, member)

            welcome_channel = guild.get_channel(cm.get_welcome_channel())

            img_path = cm.get_img_dir() + 'welcome_bg.jpg'
            img = Image.open(img_path)

            img_width = img.size[0]
            img_height = img.size[1]

            img_draw = ImageDraw.Draw(img)
            img_draw.rectangle([200, 100, img_width-200, img_height-500],
                               fill=(0, 0, 0, 128), outline=(255, 255, 255))

            msg = '¡Bienvenid@ al Servidor! @{}'.format(member.name)
            msg_font = ImageFont.truetype(
                '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf', 40)
            msg_width, msg_height = img_draw.textsize(msg, font=msg_font)
            msg_x = (img_width - msg_width)//2
            msg_y = (img_height - msg_height)//2

            img_draw.text((msg_x, msg_y), msg, fill=(0, 0, 255), font=msg_font)

            avatar = member.avatar_url_as(format='jpg', size=128)
            avatar_buffer = io.BytesIO()
            await avatar.save(avatar_buffer)
            avatar_buffer.seek(0)

            avatar_img = Image.open(avatar_buffer)
            avatar_img.resize((128, 128))

            img.paste(avatar_img, ((img_width-128)//2, (img_height-128)//2))

            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            await welcome_channel.send("**BIENVENIDAS >>** ¡Damos la bienvenida a {}!".format(member.mention), file=File(img_buffer, 'welcome_img.png'))


def setup(bot):
    bot.add_cog(VerificationSystem(bot))
    logger.info("Extension loaded: verification_system")
