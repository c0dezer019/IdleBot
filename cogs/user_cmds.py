from datetime import datetime
from discord import Member
from discord.ext import commands
from discord.utils import find
from utility.helpers import check_idle_time
import utility.request_handler as rh


class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx, member: Member):
        command = ctx.message.content.split(' ')[1]

        if not command.startswith('<@!'):
            await ctx.reply(f'Hey {ctx.message.author.mention}, I\'ll give you a response but you may not like the '
                            'results. Please use @mention for the user next time to ensure better results.\n\nTip: Users '
                            'can have the same nickname and same display name (the alphanumeric part before the '
                            'discriminator, the #).')

        if member is not None:
            response = rh.get_member(member.id)
        else:
            response = rh.get_guild(ctx.message.guild.id)

        response_as_dict = response.json()
        iso_timestamp = response_as_dict['last_activity_ts']
        status = response_as_dict['status']
        timestamp = datetime.fromisoformat(iso_timestamp)
        get_idle_time = check_idle_time(timestamp)

        if status != 'active':
            await ctx.reply(f'I\'m sorry, but {response_as_dict["name"] if member is None else response_as_dict["username"]} is not currently active.')
        else:
            idle_time_str = f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and ' \
                            f'{get_idle_time["minutes"]} ' \
                            f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'

            if get_idle_time['days'] >= 365:
                years = round(get_idle_time['days'] / 365)
                get_idle_time['days'] = get_idle_time['days'] % 365
                idle_time_str = f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and ' \
                                f'{get_idle_time["minutes"]} ' \
                                f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
                idle_time_str = f'{years} years, ' + idle_time_str

            response_str = f'Last activity for {response_as_dict["name"] if member is None else response_as_dict["username"]} was ' \
                           f'performed {idle_time_str} ago.'

            general = find(lambda x: x.name == 'general', ctx.guild.text_channels)
            sys_chan = ctx.guild.system_channel

            if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
                await sys_chan.send(response_str)
            else:
                await general.send(response_str)

    @check.error
    async def check_error_handler(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('That member was not found.')


def setup(bot):
    bot.add_cog(UserCommands(bot))
