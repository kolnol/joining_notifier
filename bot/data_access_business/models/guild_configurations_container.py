from dataclasses import dataclass, field
from typing import List

from bot.data_access_business.models.guild_configuration import GuildConfiguration


@dataclass
class GuildConfigurationsContainer:
    guild_configurations: List[GuildConfiguration] = field(default_factory=list)
