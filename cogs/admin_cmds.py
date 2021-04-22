from discord import Member
from discord.ext import commands
from discord.utils import find
import utility.request_handler as rh


def is_bot_developer():
    def predicate(ctx):
        return ctx.message.author.id == 102588778232705024

    return commands.check(predicate)


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
                'Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on')

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            pass
        elif isinstance(error, commands.MissingPermissions):
            if ctx.guild is not None:
                await ctx.guild.system_channel.send(f'Hey {ctx.message.author.mention}, this is an admin-only command.')

    @commands.command()
    async def set(self, ctx):
        # Controls the functionality of the bot per guild.
        settings = {
            'kick_idle_members': True,
            'allowed_idle_time': [1, 0, 0, 0, 0],  # Months, weeks, days, hours, minutes
        }
        pass

    @commands.command()
    @commands.has_guild_permissions(kick_members = True)
    async def ping(self, ctx, member: Member = None):
        try:
            if member.dm_channel:
                await member.dm_channel.send("Hello!")
            else:
                await member.create_dm()
                await member.dm_channel.send("hello!")

        except AttributeError:
            await ctx.reply('You must provide a member name (case-sensitive) for this command to work.')

            raise AttributeError('Missing required parameter.')

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply('That member was not found. Check spelling and try again. The name is case-sensitive '
                            'and may be easier to  just @ (mention) the user in question.')

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.reply('Unfortunately, you do not have the required role to perform this command.')

    @commands.command()
    @is_bot_developer()
    async def reload(self, ctx, cog):
        # bot_guilds = ctx.bot.guilds

        await ctx.message.guild.system_channel.send('Cog reloaded.')

        # for guild in bot_guilds:
            # await guild.system_channel.send('Hello, I have been updated. Use ?changelog to see what\'s new!')

        await ctx.bot.reload_extension(f'cogs.{cog}')

    @reload.error
    async def reload_error(self, ctx, error):

        if isinstance(error, commands.CheckFailure):
            await ctx.reply('This is a command reserved for the developer.')


def setup(bot):
    bot.add_cog(AdminCommands(bot))
