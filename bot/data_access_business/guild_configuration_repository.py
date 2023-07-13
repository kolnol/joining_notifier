from abc import ABC, abstractmethod

from bot.data_access_business.models.guild_configuration import GuildConfiguration


class GuildConfigurationRepository(ABC):

    @abstractmethod
    def get(self, guild_id: str) -> GuildConfiguration:
        pass

    @abstractmethod
    def set(self, guild_id: str, config: GuildConfiguration) -> GuildConfiguration:
        pass

    @abstractmethod
    def delete(self, guild_id: str) -> bool:
        pass
