import json

from dacite import from_dict

from bot.data_access_business.get_all_guilds_repository import GetAllGuildsRepository
from bot.data_access_business.models.guild import Guild
from bot.data_access_business.models.guild_configurations_container import GuildConfigurationsContainer


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
