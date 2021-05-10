from discord.ext.commands import Cog, command, has_guild_permissions
from discord import Embed, Member
from utils import *
from sqlalchemy import create_engine, Column, Integer, BigInteger, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

data = return_config()

engine = create_engine(
    f'postgresql://{data["database"]["username"]}:{data["database"]["password"]}@postgres_db:5432/philipposaurus',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Warn(Base):
    __tablename__ = 'warns'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    reason = Column(String)


Base.metadata.create_all(engine)


class Moderator(Cog):
    def __init__(self, client):
        self.client = client

    @command(description='Warn a member (just for Moderators)')
    @has_guild_permissions(kick_members=True)
    async def warn(self, ctx, member: Member, *, reason):
        warns = session.query(Warn).filter(Warn.user_id == member.id).first()
        if warns:
            warns.reason = f'{warns.reason}{reason};'
        else:
            warn = Warn(
                user_id=member.id
            )
            warn.reason = f'{reason};'
            session.add(warn)
        session.commit()
        warn_embed = Embed(
            title='Moderator',
            description=f'User warned: {member.mention}',
            color=colour()
        )
        warn_embed.add_field(
            name='Reason',
            value=reason
        )
        await ctx.send(embed=warn_embed)

    @command(description='Get some informations about a user (just for Moderators)')
    @has_guild_permissions(kick_members=True)
    async def user(self, ctx, member: Member):
        warns = session.query(Warn).filter(Warn.user_id == member.id).first()
        user_embed = Embed(
            title='Userinfo',
            color=colour()
        )
        user_embed.add_field(name="Mention", value=member.mention, inline=True)
        user_embed.add_field(name="Name", value=member.name, inline=True)
        user_embed.add_field(name="Nickname", value=member.nick, inline=True)
        user_embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        user_embed.add_field(name="ID", value=member.id, inline=True)
        user_embed.add_field(
            name='Guild joined',
            value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
            inline=True
        )
        user_embed.add_field(
            name='Account created',
            value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
            inline=True
        )
        try:
            reason = str(warns.reason).replace(";", "\n")
            user_embed.add_field(
                name='Warns',
                value=f'```{reason}```',
                inline=False
            )
        except AttributeError:
            pass
        user_embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=user_embed)

    @command(description='Clear many messages')
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount + 1)
        clear_embed = Embed(
            title='Clear',
            description=f'{amount} messages has been cleared',
            color=colour()
        )
        await ctx.send(embed=clear_embed, delete_after=10)


def setup(client):
    client.add_cog(Moderator(client))
