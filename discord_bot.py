
import discord
from discord import app_commands
import logging


class BotClient(discord.Client):
    def __init__(self, intents, channels_blacklist, channel_to_post_to = None):
        super().__init__(intents=intents)
        self.channel_to_post_to = channel_to_post_to
        self.channels_blacklist = channels_blacklist
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_voice_state_update(self, member, before, after):
        after_channel = after.channel

        if before.channel is None and after_channel is not None:

            if after_channel.name in channels_blacklist:
                logging.info(f'{member.name} joined {after.channel} but it was ignored because of the blacklist.')
                return

            message = f'{member.name} joined {after.channel}'
            logging.info(message)
            await self.write_to_channel(self.channel_to_post_to, message)  # TODO make it configuratble

    async def write_to_channel(self, channel_name, message):
        for guild in self.guilds:
            for channel in guild.channels:
                if channel.name == channel_name:
                    await channel.send(message)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        guild = discord.Object(id='455132185440026636')
        self.tree.copy_global_to(guild=guild) # TODO make it configurable
        await self.tree.sync(guild=guild)


if __name__ == '__main__':
    channels_blacklist = ['general']
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    client = BotClient(intents, channels_blacklist)


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
