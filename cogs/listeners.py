from discord import Game
from discord.ext import commands
from discord.utils import get
from typing import Dict
import arrow
import discord
import utility.request_handler as rh


class Listeners(commands.Cog):

    def __init__(self, bot: discord.Client):
        self.bot: discord.Client = bot
        self.ignore_list: tuple = ('?ping', '?reset', '?check')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is connected to the following guilds:')

        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')

        await self.bot.change_presence(activity = Game('Cops and Robbers'))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        chan_index: int = self.bot.guilds.index(member.guild)

        general: discord.TextChannel = get(member.guild.channels, name = 'general')
        sys_chan: discord.TextChannel = member.guild.system_channel

        if sys_chan and sys_chan.permissions_for(self.bot.guilds[chan_index].me).send_messages:
            await sys_chan.send('Welcome {0.mention}!'.format(member))
        else:
            await general.send('Welcome {0.mention}!'.format(member))

        try:
            rh.add_member(member.guild.id, member)

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            if message.content.startswith(self.ignore_list):
                return

            member_id = message.author.id
            guild_id = message.author.guild.id
            data_to_change = {
                'last_activity': message.channel.type[0],
                'last_activity_loc': message.channel.name,
                'last_activity_ts': arrow.now('US/Central').isoformat(),
                'status': 'active',
            }

            if not message.author.bot:
                try:
                    rh.update_member(member_id, **data_to_change)
                    rh.update_guild(guild_id, **data_to_change)

                except AttributeError:
                    raise

                except TypeError:
                    raise

                except ValueError:
                    raise

        elif not message.guild and str(message.channel.type) == 'private' and not message.author.bot:
            await message.channel.send(
                'Sorry, but I do not respond to DM\'s other than with this message. Try using me in a guild '
                'that I am in.')

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            if before.nick != after.nick:
                rh.update_member(after.id, **{'nickname': after.nick})
            else:
                pass

        except AttributeError:
            raise

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        try:
            if before.name != after.name or before.discriminator != after.discriminator:
                username = f'{after.name}#{after.discriminator}'

                rh.update_member(after.id, **{'username': username})
            else:
                pass

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        try:
            payload: Dict = {
                'last_activity': 'voice',
                'last_activity_loc': str(after.channel),
                'last_activity_ts': arrow.now('US/Central').isoformat()
            }

            rh.update_member(member.id, **payload)
            rh.update_guild(member.guild.id, **payload)

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        try:
            if before.name != after.name:
                rh.update_guild(after.id, **{'name': after.name})
            else:
                pass
        except Exception:
            raise


def setup(bot):
    bot.add_cog(Listeners(bot))
