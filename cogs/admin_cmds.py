# Third party modules
from nextcord import Guild, Interaction, Member, SlashOption, slash_command
from nextcord.ext.application_checks import (
    has_guild_permissions,  # pyright: ignore[reportUnknownVariableType]
)
from nextcord.ext.commands import Bot, Cog, MemberNotFound, MissingPermissions
from nextcord.utils import find

# Internal modules
from utility.request_handler import RequestHandler

rh = RequestHandler()

_NOT_IN_GUILD = "This command must be used in a server."
_OPTIONAL_MEMBER = SlashOption(required=False)


class AdminCommands(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @slash_command(name="reset", description="Resets the server data.")
    @has_guild_permissions(administrator=True)
    async def reset(self, interaction: Interaction[Bot]) -> None:
        guild: Guild | None = interaction.guild
        if guild is None:
            await interaction.response.send_message(_NOT_IN_GUILD, ephemeral=True)
            return

        data = rh.get_guild(guild.id)
        print(data)

        general = find(lambda x: x.name == "general", guild.text_channels)
        sys_chan = guild.system_channel

        if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
            await sys_chan.send(f"Activity data for {guild.name} is being reset.")
        elif general:
            await general.send(f"Activity data for {guild.name} is being reset.")

    @slash_command(name="set")
    @has_guild_permissions(administrator=True)
    async def set(self, interaction: Interaction[Bot]) -> None:
        pass

    @set.subcommand(  # pyright: ignore[reportUnknownMemberType]
        name="auto_kick", description="Kick inactive members?"
    )
    async def set_auto_kick(
        self,
        interaction: Interaction[Bot],
        enabled: bool = SlashOption(required=True),
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(_NOT_IN_GUILD, ephemeral=True)
            return

        settings = rh.get_guild(guild.id).settings
        settings.kick_inactive_members = enabled

        rh.update_guild(guild.id, settings=settings.model_dump(by_alias=True))

    @set.subcommand(
        name="time_until_inactive",
        description="How long until members should be set inactive?",
    )
    async def set_inactive(
        self,
        interaction: Interaction[Bot],
        days: int = SlashOption(default=30, min_value=7),
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(_NOT_IN_GUILD, ephemeral=True)
            return

        settings = rh.get_guild(guild.id).settings
        settings.time_before_inactive[0] = days

        rh.update_guild(guild.id, settings=settings.model_dump(by_alias=True))

    @set.subcommand(
        name="auto_prune_timer",
        description="Prune members after this long after falling inactive.",
    )
    async def auto_prune_timer(
        self,
        interaction: Interaction[Bot],
        days: int = SlashOption(default=14, min_value=7),
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(_NOT_IN_GUILD, ephemeral=True)
            return

        settings = rh.get_guild(guild.id).settings
        settings.time_before_inactive[1] = days

        rh.update_guild(guild.id, settings=settings.model_dump(by_alias=True))

    @set.error
    async def set_error(interaction: Interaction[Bot], error: Exception) -> None:
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "Unfortunately, you do not have the required permissions to perform this command."
            )

    @slash_command(name="ping")
    @has_guild_permissions(kick_members=True)
    async def ping(
        self,
        interaction: Interaction[Bot],
        member: Member | None = _OPTIONAL_MEMBER,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(_NOT_IN_GUILD, ephemeral=True)
            return

        auto_prune_timer = rh.get_guild(guild.id).settings.time_before_inactive[1]

        if member:
            dm_channel = member.dm_channel or await member.create_dm()
            await dm_channel.send(
                f"Hello!\n\nYou have currently fallen inactive in {guild.name}. "
                "If you don't return soon, you will be removed from the server. Don't worry "
                "though. If you decide to come back, you may do so.\n\n"
                f"If you do not return in {auto_prune_timer} days, you will be pruned from "
                f"{guild.name}."
            )
        elif guild.system_channel:
            await guild.system_channel.send("@everyone!")
            await guild.system_channel.send(
                "https://tenor.com/view/wake-the-fuck-up-samuel-l-jackson-wake-up-gif-5635365"
            )

    @ping.error  # pyright: ignore[reportUnknownMemberType]
    async def ping_error(interaction: Interaction[Bot], error: Exception) -> None:
        if isinstance(error, MemberNotFound):
            await interaction.response.send_message(
                "That member was not found. Check spelling and try again. The name is case-sensitive "
                "and may be easier to  just @ (mention) the user in question."
            )

        elif isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "Unfortunately, you do not have the required permissions to perform this command."
            )

    @slash_command(name="baseline")
    @has_guild_permissions(administrator=True)
    async def baseline(self, interaction: Interaction[Bot]) -> None:
        # To be performed automatically, but can also be done manually in the same way setup is done.
        # This is to establish a baseline for the server.
        # For message in messages, look for last sent message by each member in the guild and update last_activity_ts.

        pass

    @baseline.error  # pyright: ignore[reportUnknownMemberType]
    async def backlog_error(interaction: Interaction[Bot], error: Exception) -> None:
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "Unfortunately, you do not have the required permissions to perform this command."
            )


def setup(bot: Bot) -> None:
    bot.add_cog(AdminCommands(bot))
