from discord import Member
from discord.ext import commands
import utility.request_handler as rh


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def set(self, ctx):
        # Controls the functionality of the bot per guild.
        settings = {
            'kick_idle_members': True,
            'allowed_idle_time': [1, 0, 0, 0, 0],  # Months, weeks, days, hours, minutes
        }
        pass

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'Unfortunately, you do not have the required permissions to perform this command.')

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

        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'Unfortunately, you do not have the required permissions to perform this command.')

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def baseline(self, ctx):
        # To be performed automatically, but can also be done manually in the same way setup is done.
        # This is to establish a baseline for the server.
        # For message in messages, look for last sent message by each member in the guild and update last_activity_ts.
        pass

    @baseline.error
    async def backlog_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Unfortunately, you do not have the required permissions to perform this command.')


def setup(bot):
    bot.add_cog(AdminCommands(bot))
