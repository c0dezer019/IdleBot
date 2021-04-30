from datetime import datetime
from discord import Game
from discord.ext import commands
from discord.utils import find
from pytz import timezone
import utility.request_handler as rh
import json


class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ignore_list = ('?ping', '?reset', '?check')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is connected to the following guilds:')

        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')

        guilds = rh.get_guild().json()

        with open('utility/store.json', 'r+') as file:
            data = json.load(file)
            data.update(guilds)
            file.seek(0)
            json.dump(data, file, indent = 3)

        await self.bot.change_presence(activity = Game('Cops and Robbers'))

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
            rh.add_member(member.guild.id, list(member))

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            if message.content.startswith(self.ignore_list):
                return

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
        elif not message.guild and str(message.channel.type) == 'private' and not message.author.bot:
            await message.channel.send(
                'Sorry, but I do not respond to DM\'s other than with this message. Try using me in a guild '
                'that I am in.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.nickname != after.nickname:
                rh.update_member(after.id, **{'nickname': after.nick})
            else:
                pass

        except AttributeError:
            raise

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        try:
            if before.username != after.username or before.discriminator != after.discriminator:
                username = f'{after.username}#{after.discriminator}'

                rh.update_member(after.id, **{'username': username})
            else:
                pass

        except Exception:
            raise

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        pass


def setup(bot):
    bot.add_cog(Listeners(bot))
