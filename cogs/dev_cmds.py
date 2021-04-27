from discord.ext import commands
import utility.request_handler as rh


def is_bot_developer():
    def predicate(ctx):
        return ctx.message.author.id == 102588778232705024

    return commands.check(predicate)


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_bot_developer()
    async def reset(self, ctx):
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
        response = rh.add_member(guild.id, guild.members)

        if response == 200:
            await sys_chan.send(
                'Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on.')

    @commands.command()
    @is_bot_developer
    async def delete(self, ctx, obj_type, obj_id):
        pass


def setup(bot):
    bot.add_cog(DevCommands(bot))
