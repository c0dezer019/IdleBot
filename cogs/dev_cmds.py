# Third party modules
from nextcord import Interaction, Permissions, slash_command
from nextcord.ext.commands import Bot, CheckFailure, Cog, Context, command

# Internal modules
from utility.decorators.checks import slash_user_is_bot_developer, user_is_bot_developer
from utility.request_handler import RequestHandler


class DevCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.rh = RequestHandler()

    @command(hidden=True, help="")
    @user_is_bot_developer()
    async def sync(self, ctx: Context):
        if ctx.message.guild.id != 820891105322074113:
            await ctx.message.delete
        else:
            await ctx.guild.system_channel.send(ctx.message.channel.type)

    @command(
        hidden=True,
        help="If for some reason the need to start fresh occurs, this initiates the "
        "on_guild_join() procedures without having to kick and re-invite bot.",
    )
    @user_is_bot_developer()
    async def reset(self, ctx: Context):
        guild = ctx.guild
        sys_chan = guild.system_channel

        # Add guild
        response = self.rh.create_guild(guild.id, guild.name)

        if response.status_code != 200:
            await sys_chan.send(
                "I couldn't find any coffee. I no workee without coffee. Please pass a this code to my"
                f" owner: {response.status_code}"
            )
        else:
            await sys_chan.send("I'm now in business! Time to start collecting names")

        # Add members
        for member in guild.members:
            response = self.rh.member(guild.id, member)

        if response == 200:
            await sys_chan.send(
                "Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on."
            )

    @command(
        hidden=True,
        help="Deletes things from the database in the event corresponding listeners "
        "fail to do their jobs.",
    )
    @user_is_bot_developer()
    async def delete(self, ctx, obj_type: str, obj_id: int):
        pass

    @command(
        hidden=True,
        help="Loads, reloads, or unloads an extension (cog). Only the developer can use"
        "this command.",
    )
    @user_is_bot_developer()
    async def reload(self, ctx: Context, cog: str | None):
        # bot_guilds = ctx.bot.guilds

        await ctx.message.guild.system_channel.send("Cog reloaded.")

        # for guild in bot_guilds:
        # await guild.system_channel.send('Hello, I have been updated. Use ?changelog to see what\'s new!')

        await ctx.bot.reload_extension(f"cogs.{cog}")

    @reload.error
    async def reload_error(self, ctx: Context, error):
        if isinstance(error, CheckFailure):
            await ctx.reply("Sorry, but this is a command reserved for the developer.")

    @slash_command(
        default_member_permissions=Permissions(administrator=True),
        guild_ids=[820891105322074113],
        description="Sets up server in the database if there isn't one.",
    )
    @slash_user_is_bot_developer()
    async def setup(self, interaction: Interaction):
        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server", ephemeral=True
            )
            return

        if interaction.guild.system_channel:
            await interaction.guild.system_channel.send("Guild initializing.")

        self.bot.dispatch("guild_join", interaction.guild)

        await interaction.response.send_message("Guild initialization triggered.", ephemeral=True)


def setup(bot):
    bot.add_cog(DevCommands(bot))
