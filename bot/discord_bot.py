import logging

import discord
from discord import app_commands

from bot.data_access_business.get_all_guilds_repository import GetAllGuildsRepository


class BotClient(discord.Client):
    def __init__(self, intents, channels_blacklist, get_all_guilds_repo: GetAllGuildsRepository,
                 channel_to_post_to=None):
        super().__init__(intents=intents)
        self.get_all_guilds_repo = get_all_guilds_repo
        self.channel_to_post_to = channel_to_post_to
        self.channels_blacklist = channels_blacklist
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))
        await self._sync_guilds()

    async def on_voice_state_update(self, member, before, after):
        after_channel = after.channel

        if before.channel is None and after_channel is not None:

            if after_channel.name in self.channels_blacklist:
                logging.info(f'{member.name} joined {after.channel} but it was ignored because of the blacklist.')
                return

            message = f'{member.name} joined {after.channel}'
            logging.info(message)
            await self.write_to_channel(self.channel_to_post_to, message)

    async def write_to_channel(self, channel_name, message):
        for guild in self.guilds:
            for channel in guild.channels:
                if channel.name == channel_name:
                    await channel.send(message)

    # async def setup_hook(self):
    #     # This copies the global commands over to your guild.
    #     guild = discord.Object(id='455132185440026636')
    #     self.tree.copy_global_to(guild=guild) # TODO make it configurable
    #     await self.tree.sync(guild=guild)
    def _sync_guilds(self):
        guilds = self.get_all_guilds_repo.get_all()
        # TODO
