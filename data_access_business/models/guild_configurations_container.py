from dataclasses import dataclass, field
from typing import List

from data_access_business.models.guild_configuration import GuildConfiguration


@dataclass
class GuildConfigurationsContainer:
    guild_configurations: List[GuildConfiguration] = field(default_factory=list)
