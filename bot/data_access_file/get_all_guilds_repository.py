import json
import os.path
from os import listdir

from dacite import from_dict
from functional import seq

from bot.data_access_business.get_all_guilds_repository import GetAllGuildsRepository
from bot.data_access_business.models.guild import Guild
from bot.data_access_business.models.guild_configuration import GuildConfiguration


class GetAllGuildsFromFileRepository(GetAllGuildsRepository):

    def __init__(self, config_files_root_path: str) -> None:
        super().__init__()
        self.config_files_root_path = config_files_root_path

    def get_all(self) -> [Guild]:
        guilds: [Guild] = []
        guilds_jsons = seq(listdir(self.config_files_root_path)) \
            .where(lambda f: f.endswith('.json')) \
            .map(lambda f: os.path.join(self.config_files_root_path, f))

        for guilds_json in guilds_jsons:
            with open(guilds_json, 'r') as config:
                config_json = json.load(config)
                guilds_config = from_dict(data_class=GuildConfiguration, data=config_json)
                guilds.append(guilds_config.guild)

        return guilds
