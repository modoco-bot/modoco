import discord
from discord.ext import commands
from common import config
import utils
import asyncio
from typing import Optional


class VoiceChannelHandler(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.auto_generator_channel: Optional[discord.VoiceChannel] = None
        self.server_authentication_role: Optional[discord.Role] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.auto_generator_channel: discord.VoiceChannel = await utils.get_channel_by_id(self.bot, config.AUTO_VOICE_CHANNEL_GENERATOR_CHANNEL_ID)
        self.server_authentication_role = await utils.get_role_by_guild(self.auto_generator_channel.guild, config.SERVER_AUTHENTICATION_ROLE_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if not self.auto_generator_channel:
            return

        # create voice channel
        if after.channel != None and after.channel.id == self.auto_generator_channel.id:
            new_voice_channel = await member.guild.create_voice_channel(
                name=f"{member.nick or member} 님의 통화방",
                category=self.auto_generator_channel.category,
                overwrites={
                    member.guild.default_role: discord.PermissionOverwrite(manage_channels=False, connect=False, mute_members=False, kick_members=False, deafen_members=False),
                    member: discord.PermissionOverwrite(manage_channels=True, connect=True, mute_members=False, kick_members=False, deafen_members=False),
                    self.server_authentication_role: discord.PermissionOverwrite(manage_channels=False, connect=True, view_channel=True),
                }
            )
            await member.move_to(new_voice_channel)
            return

        # delete voice channel
        if before.channel and before.channel.category_id == self.auto_generator_channel.category_id and not before.channel.members and before.channel.id != self.auto_generator_channel.id:
            await asyncio.sleep(3)
            await before.channel.delete()
            return


async def setup(bot):
    await bot.add_cog(VoiceChannelHandler(bot))
