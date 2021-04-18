from datetime import datetime

import discord.ext.commands.errors
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound
from discord.utils import find
from utility.helpers import check_idle_time
import utility.request_handler as rh


class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx, member: Member = None):
        if member is not None:
            response = rh.get_member(member.id)
        else:
            response = rh.get_guild(ctx.message.guild.id)

        iso_timestamp = response['last_activity_ts']
        timestamp = datetime.fromisoformat(iso_timestamp)
        get_idle_time = check_idle_time(timestamp)
        years = 0

        if get_idle_time['days'] >= 365:
            years = round(get_idle_time['days'] / 365)
            get_idle_time['days'] = get_idle_time['days'] % 365

        idle_time_str = f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and ' \
                        f'{get_idle_time["minutes"]} minutes'

        if years > 0:
            idle_time_str = f'{years} years, ' + idle_time_str

        response_str = f'Last activity for {response.name if member is None else response.username} was performed ' \
                       f'{idle_time_str} ago.'

        await ctx.guild.system_channel.send(response_str)


def setup(bot):
    bot.add_cog(UserCommands(bot))
