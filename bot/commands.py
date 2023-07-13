import logging

import discord
from discord import app_commands

from bot.data_access_business.models.guild import Guild
from bot.data_access_business.models.guild_configuration import GuildConfiguration
from bot.discord_bot import BotClient


class CommandsConfigurator:

    @staticmethod
    def configure(client: BotClient):
        @client.tree.command(name='channel-notification-channel')
        @app_commands.describe(
            channel='The channel to post notifications to',
        )
        async def configure_notification_channel(interaction: discord.Interaction, channel: discord.TextChannel):
            guild_id = str(interaction.guild_id)
            config = client.guild_config_repository.get(guild_id)
            if config is None:
                logging.info(f'Setting up first configuration for guild {interaction.guild.name} {guild_id}')
                guild = Guild(id=interaction.guild.name, name=interaction.guild.name)
                config = GuildConfiguration(guild=guild, channel_id_to_post_to=str(channel.id))

            config.channel_id_to_post_to = str(channel.id)
            client.guild_config_repository.set(guild_id=guild_id, config=config)

            # TODO add check that bot has access to this channel
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'From now on I am posting notifications to {channel.name}')

        @app_commands.command()
        async def blacklist_show(interaction: discord.Interaction):
            guild_id = str(interaction.guild_id)
            config = client.guild_config_repository.get(guild_id)

            if config is None:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(
                    'Not configured. Please run /channel-notification-channel command to do initial setup')
                return

            embed = discord.Embed(title='Current channels which are ignored by bot')

            for channel_id in config.channel_ids_blacklist:
                channel = await client.fetch_channel(int(channel_id))
                embed.add_field(name='Name', value=channel.name)

            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(embed=embed)

        @app_commands.command()
        @app_commands.describe(
            channel='The name of the channel to ignore joinings to',
        )
        async def blacklist_add(interaction: discord.Interaction, channel: discord.VoiceChannel):
            guild_id = str(interaction.guild_id)
            config = client.guild_config_repository.get(guild_id)

            if config is None:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(
                    'Not configured. Please run /channel-notification-channel command to do initial setup')
                return
            config.channel_ids_blacklist.append(str(channel.id))
            client.guild_config_repository.set(guild_id, config)

            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'Ignoring joinings in {channel.name}')

        @app_commands.command()
        @app_commands.describe(
            channel='The name of the channel remove from blacklist',
        )
        async def blacklist_remove(interaction: discord.Interaction, channel: discord.VoiceChannel):
            guild_id = str(interaction.guild_id)
            config = client.guild_config_repository.get(guild_id)

            if config is None:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(
                    'Not configured. Please run /channel-notification-channel command to do initial setup')
                return

            config.channel_ids_blacklist.remove(channel.name)
            client.guild_config_repository.set(guild_id, config)
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f'Removed {channel.name}')

        group = discord.app_commands.Group(name='blacklist', description='Operations on channels blacklist')
        group.command(name='show')(blacklist_show.callback)
        group.command(name='add')(blacklist_add.callback)
        group.command(name='delete')(blacklist_remove.callback)
        client.tree.add_command(group)
