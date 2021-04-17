from datetime import datetime
from discord.ext import commands
from discord.utils import find
from pytz import timezone
import utility.request_handler as rh


class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        chan_index = self.bot.guilds.index(member.guild)

        general = find(lambda x: x.name == 'general', member.guild.text_channels)
        sys_chan = member.guild.system_channel

        await sys_chan.send("Hello {0.mention}!".format(member))
        await general.send('Welcome to hell, {0.mention}!'.format(member))

        if sys_chan and sys_chan.permissions_for(self.bot.guilds[chan_index].me).send_messages:
            await sys_chan.send('Welcome {0.mention}.'.format(member))
        else:
            await general.send('Welcome {0.mention}!'.format(member))

        try:
            rh.add_members()

        except ValueError:
            raise

    @commands.Cog.listener()
    async def on_message(self, message):
        member_id = message.author.id
        guild_id = message.author.guild.id
        tz = timezone('US/Central')
        local_dt = datetime.now(tz)
        data_to_change = {
            'last_activity': message.channel.type[0],
            'last_activity_loc': message.channel.name,
            'last_activity_ts': local_dt.isoformat(),
            'status': 'active',
        }

        if not message.author.bot:
            try:
                rh.update_member(member_id, **data_to_change)
                rh.update_guild(guild_id, **data_to_change)

            except AttributeError:
                raise

            except TypeError:
                raise

            except ValueError:
                raise


def setup(bot):
    bot.add_cog(Listeners(bot))
