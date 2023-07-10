from abc import ABC, abstractmethod

from bot.data_access_business.models.guild import Guild


class GetAllGuildsRepository(ABC):

    @abstractmethod
    def get_all(self) -> [Guild]:
        pass
