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
        guild_id = message.author.guild.id
        chan_type = message.channel.type
        chan = message.channel
        tz = timezone('US/Central')
        local_dt = tz.localize(datetime.now())

        if not message.author.bot:
            try:
                rh.update_timestamps(user_id, guild_id, chan_type, chan, local_dt)
            except ValueError:
                print('Something went wrong while updating user.')


def setup(bot):
    bot.add_cog(Listeners(bot))
