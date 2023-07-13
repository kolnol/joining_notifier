import logging

import discord
from discord import app_commands, Member, VoiceState

from bot.data_access_business.guild_configuration_repository import GuildConfigurationRepository
from bot.data_access_business.models.guild_configuration import GuildConfiguration


class BotClient(discord.Client):
    def __init__(self, intents, guild_config_repository: GuildConfigurationRepository):
        super().__init__(intents=intents)
        self.guild_config_repository = guild_config_repository
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        guild_id = str(member.guild.id)
        config = self.guild_config_repository.get(guild_id)
        if config is None:
            logging.warning(f'There is no configuration for guild {guild_id}. Ignoring.')
            return

        await self.notify_joiner(member, before, after, config)

    async def notify_joiner(self, member: Member, before: VoiceState, after: VoiceState, config: GuildConfiguration):
        after_channel = after.channel

        if before.channel is None and after_channel is not None:
            if str(after_channel.id) in config.channel_ids_blacklist:
                logging.info(
                    f'{member.name} joined {after.channel} in guild {member.guild} but\
                     it was ignored because of the blacklist.')
                return

            message = f'{member.name} joined {after.channel} in guild {member.guild}'
            logging.info(message)
            await self.write_to_channel(config.channel_id_to_post_to, message)

    async def write_to_channel(self, channel_id, message):
        channel = await self.fetch_channel(channel_id)
        if channel is None:
            logging.error(f'Channel with id {channel_id} is not found.')
            return
        await channel.send(message)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # self.tree.fallback_to_global()  # TODO make it configurable
        MY_GUILD = discord.Object(id=455132185440026636)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        await self.tree.sync()
