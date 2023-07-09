import dataclasses
import json

from dacite import from_dict

from data_access_business.get_all_guilds_repository import GetAllGuildsRepository
from data_access_business.models.guild import Guild
from data_access_business.models.guild_configuration import GuildConfiguration
from data_access_business.models.guild_configurations_container import GuildConfigurationsContainer


class GetAllGuildsFromFileRepository(GetAllGuildsRepository):

    def __init__(self, config_file_path: str) -> None:
        super().__init__()
        self.config_file_path = config_file_path

    def get_all(self) -> [Guild]:
        guilds: [Guild] = []
        with open(self.config_file_path, 'r') as config:
            config_json = json.load(config)
            guilds_configs = from_dict(data_class=GuildConfigurationsContainer, data=config_json)
            for guild_config in guilds_configs.guild_configurations:
                guilds.append(guild_config.guild)

        return guilds


if __name__ == '__main__':
    guilds_configs = GuildConfigurationsContainer()
    guilds_configs.guild_configurations.append(
        GuildConfiguration(guild=Guild(name='Test', id='test-id'), channel_id_to_post_to='general'))
    guilds_configs.guild_configurations.append(
        GuildConfiguration(guild=Guild(name='Test2', id='test-id2'), channel_id_to_post_to='general2'))

    test_config_path = 'test_db.json'
    with open(test_config_path, 'w') as fp:
        json.dump(dataclasses.asdict(guilds_configs), fp)

    repo = GetAllGuildsFromFileRepository(test_config_path)
    guilds = repo.get_all()

    print(guilds)
