# Third party modules
from nextcord import Guild
from nextcord.ext.commands import Bot, Cog
from nextcord.utils import find

# Internal modules
from main import redis
from utility.request_handler import RequestHandler

rh = RequestHandler()


class Setup(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        general = find(lambda x: x.name == "general", guild.text_channels)
        sys_chan = guild.system_channel

        if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
            await sys_chan.send(
                f"Hello {guild.name}! I am here to take names and drink coffee, but I am all out of coffee. Please "
                "wait while I get a refill."
            )
        else:
            await general.send(
                f"Hello {guild.name}! I am here to take names and drink coffee, but I am all out of coffee. Please "
                "wait while I get a refill."
            )

    @Cog.listener("on_guild_join")
    async def setup(self, guild: Guild):
        sys_chan = guild.system_channel
        response = rh.create_guild(guild.id, guild.name)

        if response["createGuild"]["code"] != 200:
            await sys_chan.send(
                "I couldn't find any coffee. I no workee without coffee. Please pass this code to my"
                f" owner: {response.status_code}"
            )
        else:
            if not await redis.exists(f"guild:{guild.id}:meta"):
                meta = {
                    "guild_id": response["createGuild"]["guild"]["guildId"],
                    "name": guild.name,
                    "status": response["createGuild"]["guild"]["status"],
                    "date_added": response["createGuild"]["guild"]["dateAdded"],
                }

                await redis.hset(f"guild:{guild.id}:meta", mapping=meta)

            await sys_chan.send("I'm now in business! Time to start collecting names")

            pipe = redis.pipeline()

            for member in guild.members:
                if member.bot:
                    continue

                m_response = rh.create_member(guild.id, member.id, member.name)

                if m_response["createMember"]["code"] != 200:
                    await sys_chan.send(
                        f"My pencil broke and I'm unable to write names. Received code {response['code']} from server."
                    )
                    break

                if not await redis.sismember(f"guild:{guild.id}:members", member.id):
                    await redis.sadd(f"guild:{guild.id}:members", member.id)
                    r_data = {
                        k: "" if v is None else str(v)
                        for k, v in m_response["createMember"]["member"].items()
                    }

                    r_data["name"] = member.display_name
                    pipe.hset(
                        f"guild:{guild.id}:member:{member.id}",
                        mapping=r_data,
                    )

            if len(pipe.command_stack) > 0:
                await pipe.execute()

            await sys_chan.send(
                "Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on"
            )


def setup(bot):
    bot.add_cog(Setup(bot))
