import json
from typing import Optional

from dacite import from_dict
from sqlalchemy.orm import Session

from bot.data_access_business.guild_configuration_repository import GuildConfigurationRepository
from bot.data_access_business.models.guild_configuration import GuildConfiguration
from bot.data_access_sql.engine_init import engine
from bot.data_access_sql.models.guild_configuration_entity import GuildConfigurationEntity


class GuildConfigurationFromFileRepository(GuildConfigurationRepository):
    def set(self, guild_id: str, config: GuildConfiguration) -> GuildConfiguration:
        pass

    def delete(self, guild_id: str) -> bool:
        pass

    def get(self, guild_id: str) -> GuildConfiguration:
        config_entity: Optional[GuildConfigurationEntity] = None

        with Session(engine) as session:
            config_entity = session.query(GuildConfigurationEntity).get(guild_id)
            if config_entity is None:
                raise KeyError(f'No configuration found for guild id {guild_id}')

        config_json = config_entity.config
        config_json = json.loads(config_json)
        config: GuildConfiguration = from_dict(data_class=GuildConfiguration, data=config_json)
        
        return config
