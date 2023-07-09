from dataclasses import dataclass, field
from typing import List

from data_access_business.models.guild import Guild


@dataclass
class GuildConfiguration:
    guild: Guild
    channel_id_to_post_to: str
    channel_ids_blacklist: List[str] = field(default_factory=list)
