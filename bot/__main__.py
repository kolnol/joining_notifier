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

    client.run('MTEyMzczMTI1MTU1NjI2MTk0OA.G-z5au.KZ8dkb0J4VcMFw1_WKdV3-LVuGSqUiPkrGhdn4')
