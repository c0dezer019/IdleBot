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
        try:
            chan_index = self.bot.guilds.index(member.guild)

            general = find(lambda x: x.name == 'general', member.guild.text_channels)
            sys_chan = member.guild.system_channel

            await sys_chan.send("Hello {0.mention}!".format(member))
            await general.send('Welcome to hell, {0.mention}!'.format(member))

            if sys_chan and sys_chan.permissions_for(self.bot.guilds[chan_index].me).send_messages:
                await sys_chan.send('Welcome {0.mention}.'.format(member))
            else:
                await general.send('Welcome {0.mention}!'.format(member))

        except ValueError:
            print("That guild doesn't exist")

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        server_id = message.author.guild.id
        tz = timezone('US/Central')
        local_dt = tz.localize(datetime.now())
        data_to_change = {
            'last_activity': message.channel.type[0],
            'last_activity_loc': message.channel.name,
            'last_activity_ts': local_dt.isoformat(),
        }

        if not message.author.bot:
            try:
                rh.update_user(user_id, **data_to_change)
                rh.update_server(server_id, **data_to_change)
            except ValueError:
                print('Something went wrong while updating user.')


def setup(bot):
    bot.add_cog(Listeners(bot))
