import discord
from datetime import datetime
from discord.ext import commands
from discord.utils import find
from typing import Dict
from requests import Response
from utility.helpers import check_idle_time
import utility.request_handler as rh


class UserCommands(commands.Cog):

    def __init__(self, bot: discord.Client):
        self.bot: discord.Client = bot

    help_lib: Dict = {
        'check_brief': 'Returns the idle time of a specified user, or the guild if no user is mentioned.',
        'check_help': 'Syntax: ?check @<user: Optional>\n\nThis command can be shorted to ch. In order for it '
                      'to work correctly, you should mention the user, however, as long as the given name '
                      'matches a member in the guild, it will work, but as members can have the same nicknames/'
                      'usernames it may not give the correct results.',
        'performance_brief': 'Provides performance stats of the bot.',
        'performance_help': 'Syntax: ?performance\n\nCan be shorted to "per". This command returns various '
                             'performance stats for the bot such as latency between bot and Discord API and latency '
                             'the bot\'s front and backend.'

    }

    @commands.command(aliases = ['ch'], brief = help_lib['check_brief'], help = help_lib['check_help'])
    async def check(self, ctx: commands.Context, member: discord.Member):
        command = ctx.message.content.split(' ')[1]

        if not command.startswith('<@!'):
            await ctx.reply(f'Hey {ctx.message.author.mention}, I\'ll give you a response but you may not like the '
                            'results. Please use @mention for the user next time to ensure better results.\n\nTip: Users '
                            'can have the same nickname and same display name (the alphanumeric part before the '
                            'discriminator, the #).')

        if member is not None:
            response: Response = rh.get_member(member.id)
        else:
            response: Response = rh.get_guild(ctx.message.guild.id)

        response_as_dict: Dict = response.json()['member' if member else 'guild']
        iso_timestamp: str = response_as_dict['last_activity_ts']
        status: str = response_as_dict['status']
        timestamp: datetime = datetime.fromisoformat(iso_timestamp)
        get_idle_time: Dict = check_idle_time(timestamp)

        if status != 'active':
            await ctx.reply(f'I\'m sorry, but {response_as_dict["name"] if member is None else response_as_dict["username"]} is not currently active.')
        else:
            idle_time: str = f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and ' \
                                 f'{get_idle_time["minutes"]} ' \
                                 f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'

            if get_idle_time['days'] >= 365:
                years = round(get_idle_time['days'] / 365)
                get_idle_time['days'] = get_idle_time['days'] % 365
                idle_time: str = f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and ' \
                                 f'{get_idle_time["minutes"]} ' \
                                 f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
                idle_time: str = f'{years} years, ' + idle_time

            response_str: str = f'Last activity for {response_as_dict["name"] if member is None else response_as_dict["username"]} was ' \
                                f'performed {idle_time} ago.'

            general: discord.TextChannel = find(lambda x: x.name == 'general', ctx.guild.text_channels)
            sys_chan: discord.TextChannel = ctx.guild.system_channel

            if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
                await sys_chan.send(response_str)
            else:
                await general.send(response_str)

    @check.error
    async def check_error_handler(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('That member was not found.')

    @commands.command(aliases = ['per'], brief = help_lib['performance_brief'], help = help_lib['performance_help'])
    async def performance(self, ctx: commands.Context):
        pass


def setup(bot):
    bot.add_cog(UserCommands(bot))
