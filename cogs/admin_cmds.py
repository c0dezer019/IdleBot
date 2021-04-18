from discord import Member
from discord.ext import commands
from discord.utils import find
import utility.request_handler as rh


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def setup(self, ctx):
        general = find(lambda x: x.name == 'general', ctx.guild.text_channels)
        sys_chan = ctx.guild.system_channel

        if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
            await sys_chan.send(
                'Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                'wait while I get a refill.'.format(ctx.guild.name))
        else:
            await general.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                               'wait while I get a refill.'.format(ctx.guild.name))

        # Add guild
        guild_info = { 'guild_id': ctx.guild.id, 'name': ctx.guild.name }
        response = rh.add_guild(guild_info)

        if response.status_code != 200:
            await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a this code to my'
                                ' owner: {0}'.format(response.status_code))
        else:
            await sys_chan.send('I\'m now in business! Time to start collecting names')

        # Add members
        response = rh.add_member(ctx.guild.id, ctx.guild.members)

        if response == 200:
            await sys_chan.send(
                'Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry'
                ' on')

    @commands.command()
    async def set(self, ctx):
        # Controls the functionality of the bot per guild.
        settings = {
            'kick_idle_members': True,
            'allowed_idle_time': [1, 0, 0, 0, 0],  # Months, weeks, days, hours, minutes
        }
        pass

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def ping(self, ctx, member: Member = None):
        general = find(lambda x: x.name == 'general', ctx.guild.text_channels)
        sys_chan = ctx.guild.system_channel

        try:
            if member.dm_channel:
                await member.dm_channel.send("Hello!")
            else:
                await member.create_dm()
                await member.dm_channel.send("hello!")

        except AttributeError:
            if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
                await sys_chan.send(f'{ctx.message.author.mention}, you must provide a member name (case-sensitive) '
                                    f'for this command to work.')
            else:
                await general.send(f'{ctx.message.author.mention}, you must provide a member name (case-sensitive) '
                                   f'for this command to work.')

            raise AttributeError('Missing required parameter.')

    @ping.error
    async def ping_error(self, ctx, error):
        general = find(lambda x: x.name == 'general', ctx.guild.text_channels)
        sys_chan = ctx.guild.system_channel

        if isinstance(error, commands.MemberNotFound):
            if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
                await sys_chan.send(f'{ctx.message.author.mention}, that member was not found. Check spelling and try '
                                    f'again. The name is case-sensitive and may be easier to  just @ (mention) the user'
                                    f' in question.')
            else:
                await general.send(f'{ctx.message.author.mention}, was not found. Check spelling and try '
                                   f'again. The name is case-sensitive and may be easier to  just @ (mention) the user '
                                   f'in question.')


def setup(bot):
    bot.add_cog(AdminCommands(bot))
