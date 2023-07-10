import dataclasses
import json
import logging
import os

from bot.data_access_business.models.guild import Guild
from bot.data_access_business.models.guild_configuration import GuildConfiguration
from bot.data_access_business.models.guild_configurations_container import GuildConfigurationsContainer
from bot.data_access_file.get_all_guilds_repository import GetAllGuildsFromFileRepository


def setup_module(module):
    """setup any state specific to the execution of the given module."""
    global test_config_path
    test_config_path = 'test_db.json'


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    logging.info('Cleanup')
    if os.path.isfile(test_config_path):
        os.remove(test_config_path)
    else:
        # If it fails, inform the user.
        logging.error("Error: %s file not found" % test_config_path)


def test_can_get_guilds():
    # prepare
    guilds_configs = GuildConfigurationsContainer()
    expected_guilds = [Guild(name='Test', id='test-id'), Guild(name='Test2', id='test-id2')]

    for expected_guild in expected_guilds:
        guilds_configs.guild_configurations.append(
            GuildConfiguration(guild=expected_guild, channel_id_to_post_to='general'))

    with open(test_config_path, 'w') as fp:
        json.dump(dataclasses.asdict(guilds_configs), fp)

    # act
    repo = GetAllGuildsFromFileRepository(test_config_path)
    guilds = repo.get_all()

    # assert
    assert len(guilds) == 2
    assert guilds == expected_guilds
