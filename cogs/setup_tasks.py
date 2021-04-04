from discord.ext import commands
from discord import Game
from discord.utils import find
import utility.request_handler as rh


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is connected to the following guilds:')

        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')

        await self.bot.change_presence(activity = Game('Cops and Robbers'))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        sys_chan = guild.system_channel

        if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
            await sys_chan.send(
                'Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                'wait while I get a refill.'.format(guild.name))
        else:
            await general.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                               'wait while I get a refill.'.format(guild.name))

        # Add server
        guild_info = { 'server_id': guild.id, 'name': guild.name }
        response = rh.add_server(guild_info)

        if response != 200:
            await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a this code to my'
                                ' owner: {0}'.format(response.status_code))
        else:
            await sys_chan.send('I\'m now in business! Time to start collecting names')

        # if users don't match guild members, add member to the database.
        user_packet = { 'server_id': guild.id, 'users': guild.members }
        response = rh.handle_users(user_packet)

        if response == 200:
            await sys_chan.send(
                'Names have been collected, eyeglasses have been cleaned, bunnies have been killed. Carry'
                ' on')
        elif type(response) == tuple:
            await sys_chan.send('Some names were collected, but I couldn\'t understand some of this gibberish. The '
                                'Here, I made some weird notes: {}'.format(response[1]))
