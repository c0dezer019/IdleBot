# Standard modules
from typing import Optional

# Third party modules
from discord import Member
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    MemberNotFound,
    MissingPermissions,
    command,
    has_guild_permissions,
)


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    @has_guild_permissions(administrator=True)
    async def set(self, ctx: Context):
        # Controls the functionality of the bot per guild.
        """settings = {
            "kick_inactive_members": True,
            "time_before_inactive": [
                1,
                0,
                0,
                0,
                0,
            ],  # Months, weeks, days, hours, minutes
        }"""

    @set.error
    async def set_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "Unfortunately, you do not have the required permissions to perform this command."
            )
        elif type(ctx.message) is not int:
            await ctx.reply(
                f"'{ctx.message}' is not a valid entry. Argument should be a whole "
                "number."
            )

    @command()
    @has_guild_permissions(kick_members=True)
    async def ping(self, ctx: Context, member: Optional[Member]):
        try:
            if member.dm_channel:
                await member.dm_channel.send("Hello!")
            else:
                await member.create_dm()
                await member.dm_channel.send("hello!")

        except AttributeError as exc:
            await ctx.reply(
                "You must provide a member name (case-sensitive) for this command to work."
            )

            raise AttributeError("Missing required parameter.") from exc

    @ping.error
    async def ping_error(self, ctx: Context, error):
        if isinstance(error, MemberNotFound):
            await ctx.reply(
                "That member was not found. Check spelling and try again. The name is case-sensitive "
                "and may be easier to  just @ (mention) the user in question."
            )

        elif isinstance(error, MissingPermissions):
            await ctx.reply(
                "Unfortunately, you do not have the required permissions to perform this command."
            )

    @command()
    @has_guild_permissions(administrator=True)
    async def baseline(self, ctx: Context):
        # To be performed automatically, but can also be done manually in the same way setup is done.
        # This is to establish a baseline for the server.
        # For message in messages, look for last sent message by each member in the guild and update last_activity_ts.
        pass

    @baseline.error
    async def backlog_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "Unfortunately, you do not have the required permissions to perform this command."
            )


def setup(bot):
    bot.add_cog(AdminCommands(bot))
