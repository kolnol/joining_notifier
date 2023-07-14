import os

import discord

from bot.commands import CommandsConfigurator
from bot.data_access_file.guild_configuration_repository import GuildConfigurationFromFileRepository
from bot.discord_bot import BotClient

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    config_path = 'db'
    repo = GuildConfigurationFromFileRepository(config_path)
    client = BotClient(intents, repo)
    CommandsConfigurator.configure(client)

    token = os.environ.get('DISCORD_TOKEN')
    if token is None:
        raise ValueError('Token is empty. Please set DISCORD_TOKEN env variable.')
    client.run(token)
