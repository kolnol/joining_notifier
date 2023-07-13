import dataclasses
import json
import os.path
from typing import Optional

from dacite import from_dict

from bot.data_access_business.guild_configuration_repository import GuildConfigurationRepository
from bot.data_access_business.models.guild_configuration import GuildConfiguration


# TODO build a semaphore for concurrent access?
class GuildConfigurationFromFileRepository(GuildConfigurationRepository):
    def __init__(self, config_files_root_path: str) -> None:
        super().__init__()
        self.config_files_root_path = config_files_root_path

    def set(self, guild_id: str, config: GuildConfiguration) -> GuildConfiguration:
        file_path = os.path.join(self.config_files_root_path, f'{guild_id}.json')
        config.guild.id = guild_id

        with open(file_path, 'w+') as config_file:
            json.dump(dataclasses.asdict(config), config_file)

        return config

    def delete(self, guild_id: str) -> bool:
        file_path = os.path.join(self.config_files_root_path, f'{guild_id}.json')
        if os.path.exists(file_path):
            os.remove(file_path)
        return True

    def get(self, guild_id: str) -> Optional[GuildConfiguration]:
        file_path = os.path.join(self.config_files_root_path, f'{guild_id}.json')
        config: GuildConfiguration = None

        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as config_file:
            config_json = json.load(config_file)
            config = from_dict(data_class=GuildConfiguration, data=config_json)

        return config
