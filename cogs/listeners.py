import datetime

from discord import Game
from discord.ext import commands
from discord.utils import get
from typing import Dict
from utility.helpers import check_idle_time
import arrow
import discord
import json
import logging
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

        print()  # An empty line for formatting.

        guilds = rh.get_guild().json()['guilds']

        with open('utility/storeTest.json', 'w') as file:
            json.dump(guilds, file, indent = 3)

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

            if not message.author.bot:
                dt: arrow.Arrow = arrow.now('US/Central')
                get_idle_time: dict = check_idle_time(dt.datetime)

                with open('utility/storeTest.json', 'r') as file:
                    data: Dict = json.load(file)

                guild_index: int = next((index for (index, d) in enumerate(data)
                                         if d['guild_id'] == message.guild.id), None)
                member_index: int = next((index for (index, d) in enumerate(data[guild_index]['members'])
                                          if d['member_id'] == message.author.id), None)
                data: dict = {
                    'guild': data['guilds'][guild_index],
                    'member': data['guilds'][guild_index]['members'][member_index]
                }

                for k in data.keys():
                    k['idle_times'].append(get_idle_time)  # History of times idle.
                    k['idle_time_avg'] = sum(k['idle_times'])/len(k['idle_times'])  # Current idle time averages
                    k['idle_time_avgs'].append(k['idle_time_avg'])  # Past averages

                    if len(k['idle_times']) > 50:
                        k['idle_times'].remove(k['idle_times'][0])

        elif not message.guild and str(message.channel.type) == 'private' and not message.author.bot:
            await message.channel.send(
                'Sorry, but I do not respond to DM\'s other than with this message. Try using me in a guild '
                'that I am in.')

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            if before.nick != after.nick:
                rh.update_member(after.id, **{ 'nickname': after.nick })
            else:
                pass

        except AttributeError:
            raise

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        try:
            if before.name != after.name or before.discriminator != after.discriminator:
                username = f'{after.name}#{after.discriminator}'

                rh.update_member(after.id, **{ 'username': username })
            else:
                pass

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):

        with open('utility/storeTest.json', 'rw') as file:
            data: Dict = json.load(file)

        guild_index: int = next((index for (index, d) in enumerate(data)
                                 if d['guild_id'] == member.guild.id), None)
        member_index: int = next((index for (index, d) in enumerate(data[guild_index]['members'])
                                  if d['member_id'] == member.id), None)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        try:
            if before.name != after.name:
                rh.update_guild(after.id, **{ 'name': after.name })
            else:
                pass
        except Exception:
            raise


def setup(bot):
    bot.add_cog(Listeners(bot))
