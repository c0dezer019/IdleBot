from discord.ext import commands
from src.utility.helpers import check_idle_time, filter_channels, get_user_last_message, get_messages, generate_idle_msg


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def ping(self, ctx, args):
        members = ctx.message.guild.members
        user = ''

        if args:
            for i, v in enumerate(members):
                if args == v.name:
                    user = v
                    break

            if not user:
                await ctx.channel.send(f'{args} is not a valid user or has changed their name.')

        text_channels = filter_channels(ctx.message.guild.channels)
        all_messages = await get_messages(text_channels)
        user_last_message = get_user_last_message(all_messages, user)
        time_idle = check_idle_time(user_last_message.created_at.replace(tzinfo = None))
        response = generate_idle_msg(time_idle)

        # if user has no recent activity, label as inactive.
        # if user has recent activity, update the appropriate fields in the database.

        await ctx.channel.send(f'{user.name}' + response)
