# Standard modules
from typing import Optional

# Third party modules
from nextcord import Interaction, Member, SlashOption
from nextcord.ext.commands import (
    Bot,
    Cog,
    Context,
    MemberNotFound,
    MissingPermissions,
    has_guild_permissions,
    slash_command,
)

# Internal modules
from utility import request_handler as rh


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @slash_command(name = "set")
    @has_guild_permissions
    async def set(interaction: Interaction):
        pass


    @set.subcommand(name = "AutoKick", description = "Kick inactive members?")
    async def set_auto_kick(
        interaction: Interaction,
        enabled: bool = SlashOption(required = True)
    ):
        guild_settings = rh.get_guilds(interaction.guild.id)["guild"]["settings"]
        guild_settings["auto_kick"] = enabled

        rh.update_guild(interaction.guild.id, **{"settings": guild_settings})


    @set.subcommand(name = "TimeUntilInactive", description = "How long until members should be set inactive?")
    async def set_inactive(
        interaction: Interaction,
        days: int = SlashOption(default = 30, min_value = 7),
    ):
        guild_settings: dict = rh.get_guilds(interaction.guild.id)["guild"]["settings"]
        guild_settings["set_inactive"] = days

        rh.update_guild(interaction.guild.id, **{"settings": guild_settings})


    @set.subcommand(name = "AutoPruneTimer", description = "Prune members after this long after falling inactive.")
    async def auto_prune_timer(
        interaction: Interaction,
        days: int = SlashOption(default = 14, min_value = 7),
    ):
        guild_settings: dict = rh.get_guilds(interaction.guild.id)["guild"]["settings"]
        guild_settings["auto_prune_timer"] = days

        rh.update_guild(interaction.guild.id, **{"settings": guild_settings})

    @set.error
    async def set_error(interaction: Interaction, error):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "Unfortunately, you do not have the required permissions to perform this command."
            )


    @slash_command(name = "ping")
    @has_guild_permissions(kick_members = True)
    async def ping(
        interaction: Interaction,
        member: Optional[Member] = SlashOption(required = False)
    ):
        auto_prune_timer: bool = rh.get_guilds(interaction.guild.id)["guild"]["settings"]["auto_prune_timer"]

        if member:
            if member.dm_channel:
                await member.dm_channel.send("Hello!")
            else:
                await member.create_dm()
                await member.dm_channel.send(f'Hello!\n\nYou have currently fallen inactive in {interaction.guild.name}. '
                                             'If you don\'t return soon, you will be removed from the server. Don\'t worry '
                                             'though. If you decide to come back, you may do so.\n\n'
                                             f'If you do not return in {auto_prune_timer} days, you will be pruned from '
                                             f'{interaction.guild.name}.'
                                            )
        else:
            interaction.guild.system_channel.send("@everyone!")
            interaction.guild.system_channel.send("https://tenor.com/view/wake-the-fuck-up-samuel-l-jackson-wake-up-gif-5635365")


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


    @slash_command(name = "baseline")
    @has_guild_permissions(administrator = True)
    async def baseline(interaction: Interaction):
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
