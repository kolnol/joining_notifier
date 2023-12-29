from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class GuildEntity(Base):
    __tablename__ = 'guilds'

    id = mapped_column(Integer, primary_key=True)


class GuildConfigurationEntity(Base):
    __tablename__ = 'configurations'

    guild_id = mapped_column(Integer, ForeignKey(GuildEntity.id), primary_key=True)
    config = mapped_column(String)
