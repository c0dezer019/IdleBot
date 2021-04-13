from discord.ext import commands
from utility.helpers import check_idle_time, filter_channels, get_user_last_message, get_messages, generate_idle_msg
import utility.request_handler as rh


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def ping(self, ctx, args):
        pass


def setup(bot):
    bot.add_cog(UserCommands(bot))
