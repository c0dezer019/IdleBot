from discord.ext import commands
from typing import Optional
import utility.request_handler as rh


def is_bot_developer():
    def predicate(ctx: commands.Context):
        return ctx.message.author.id == 102588778232705024

    return commands.check(predicate)


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True, help = 'If for some reason the need to start fresh occurs, this initiates the '
                                            'on_guild_join() procedures without having to kick and re-invite bot.')
    @is_bot_developer()
    async def reset(self, ctx: commands.Context):
        guild = ctx.guild
        sys_chan = guild.system_channel

        # Add guild
        guild_info = { 'guild_id': guild.id, 'name': guild.name }
        response = rh.add_guild(guild_info)

        if response.status_code != 200:
            await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a this code to my'
                                ' owner: {0}'.format(response.status_code))
        else:
            await sys_chan.send('I\'m now in business! Time to start collecting names')

        # Add members
        for member in guild.members:
            response = rh.add_member(guild.id, member)

        if response == 200:
            await sys_chan.send(
                'Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on.')

    @commands.command(hidden = True, help = 'Deletes things from the database in the event corresponding listeners '
                                            'fail to do their jobs.')
    @is_bot_developer()
    async def delete(self, ctx, obj_type: str, obj_id: int):
        pass

    @commands.command(hidden = True, help = 'Loads, reloads, or unloads an extension (cog). Only the developer can use'
                                            'this command.')
    @is_bot_developer()
    async def reload(self, ctx: commands.Context, cog: Optional[str]):
        # bot_guilds = ctx.bot.guilds

        await ctx.message.guild.system_channel.send('Cog reloaded.')

        # for guild in bot_guilds:
        # await guild.system_channel.send('Hello, I have been updated. Use ?changelog to see what\'s new!')

        await ctx.bot.reload_extension(f'cogs.{cog}')

    @reload.error
    async def reload_error(self, ctx: commands.Context, error):

        if isinstance(error, commands.CheckFailure):
            await ctx.reply('Sorry, but this is a command reserved for the developer.')


def setup(bot):
    bot.add_cog(DevCommands(bot))
