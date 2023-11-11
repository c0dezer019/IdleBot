# Standard modules
import datetime
from typing import Dict, Optional

# Third party modules
import arrow
from nextcord import Interaction, Member, SlashOption, slash_command
from nextcord.ext.commands import Bot, Cog
from requests import Response

# Internal modules
import utility.request_handler as rh
from utility.helpers import _check_time_idle


class UserCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    help_lib: Dict = {
        "member_status": "member: Returns idle time of the specified member",
        "guild_status": "Returns the idle time of the guild",
        "bot_performance": "Performance stats for the bot",
        "guild_health": "Provides a link to a page that contains various graphs "
        "and charts to illustrate the overall activity of a server.",
    }


    @slash_command(name="status")
    async def status_command(self, interaction: Interaction):
        pass


    @status_command.subcommand(name = "member", description = help_lib["member_status"])
    async def member_status_command(
        self,
        interaction: Interaction,
        member: Optional[Member] = SlashOption(required=False)
    ):
        response: Response = rh.get_members(member.id)

        response_as_dict: Dict = response.json()["member"]
        iso_timestamp: str = response_as_dict["last_activity_ts"]
        status: str = response_as_dict["status"]
        timestamp: datetime.datetime = arrow.get(iso_timestamp).datetime
        get_idle_time: Dict = _check_time_idle(timestamp)

        if status != "active":
            await interaction.response.send_message(
                f'I\'m sorry, but {response_as_dict["username"]} is not currently active.'
            )
        else:
            idle_time: str = (
                f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and '
                f'{get_idle_time["minutes"]} '
                f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
            )

            if get_idle_time["days"] >= 365:
                years = round(get_idle_time["days"] / 365)
                get_idle_time["days"] = get_idle_time["days"] % 365
                idle_time: str = (
                    f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and '
                    f'{get_idle_time["minutes"]} '
                    f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
                )
                idle_time: str = f"{years} years, " + idle_time

            response_str: str = (
                f'Last activity for {response_as_dict["username"]} was '
                f"performed {idle_time} ago."
            )

            await interaction.response.send_message(response_str)


    @status_command.subcommand(name = "guild", description = help_lib["guild_status"])
    async def guild_status_command(self, interaction: Interaction):
        response: Response = rh.get_guilds(interaction.guild.id)

        response_as_dict: Dict = response.json()["guild"]
        iso_timestamp: str = response_as_dict["last_activity_ts"]
        status: str = response_as_dict["status"]
        timestamp: datetime.datetime = arrow.get(iso_timestamp).datetime
        get_idle_time: Dict = _check_time_idle(timestamp)

        if status != "active":
            await interaction.response.send_message(
                f'I\'m sorry, but {response_as_dict["name"]} is not currently active.'
            )
        else:
            idle_time: str = (
                f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and '
                f'{get_idle_time["minutes"]} '
                f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
            )

            if get_idle_time["days"] >= 365:
                years = round(get_idle_time["days"] / 365)
                get_idle_time["days"] = get_idle_time["days"] % 365
                idle_time: str = (
                    f'{get_idle_time["days"]} days, {get_idle_time["hours"]} hours, and '
                    f'{get_idle_time["minutes"]} '
                    f'{"minutes" if get_idle_time["minutes"] > 1 or get_idle_time["minutes"] == 0 else "minute"}'
                )
                idle_time: str = f"{years} years, " + idle_time

            response_str: str = (
                f'Last activity for {response_as_dict["name"]} was '
                f"performed {idle_time} ago."
            )

            await interaction.response.send_message(response_str)


    @slash_command(name = "bot_performance_check", description = help_lib["bot_performance"])
    async def performance_check_command(self, interaction: Interaction):
        pass


    @slash_command(name="guild_health", description=["guild_health"])
    async def guild_health(self, interaction: Interaction):
        pass


def setup(bot):
    bot.add_cog(UserCommands(bot))
