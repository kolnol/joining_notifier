import discord
from discord import app_commands

from bot.data_access_file.get_all_guilds_repository import GetAllGuildsFromFileRepository
from bot.discord_bot import BotClient

if __name__ == '__main__':
    channels_blacklist = ['general']
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    config_path = 'db.json'
    repo = GetAllGuildsFromFileRepository(config_path)
    client = BotClient(intents, channels_blacklist, repo)


    @client.tree.command(name='channel-notification-channel')
    @app_commands.describe(
        channel='The name of the channel to post notifications to',
    )
    async def configure_notification_channel(interaction: discord.Interaction, channel: discord.TextChannel):
        client.channel_to_post_to = channel.name
        # TODO add check that bot has access to this channel
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Posting notifications to {channel.name}')


    @client.tree.command()
    async def blacklist_show(interaction: discord.Interaction):
        embed = discord.Embed(title='Current channels which are ignored by bot')
        for channel_name in client.channels_blacklist:
            embed.add_field(name='Name', value=channel_name)

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(embed=embed)


    @client.tree.command()
    @app_commands.describe(
        channel='The name of the channel to ignore joinings to',
    )
    async def blacklist_add(interaction: discord.Interaction, channel: discord.VoiceChannel):
        client.channels_blacklist.append(channel.name)

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Ignoring joinings in {channel.name}')


    @client.tree.command()
    @app_commands.describe(
        channel='The name of the channel remove from blacklist',
    )
    async def blacklist_remove(interaction: discord.Interaction, channel: discord.VoiceChannel):
        client.channels_blacklist.remove(channel.name)

        # noinspection PyUnresolvedReferences
        await interaction.response.send_message(f'Removed {channel.name}')


    client.run('MTEyMzczMTI1MTU1NjI2MTk0OA.G-z5au.KZ8dkb0J4VcMFw1_WKdV3-LVuGSqUiPkrGhdn4')
