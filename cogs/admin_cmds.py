from discord.ext import commands
from discord.utils import find
import utility.request_handler as rh


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command()
def setup(self, ctx):
    general = find(lambda x: x.name == 'general', ctx.guild.text_channels)
    sys_chan = ctx.guild.system_channel

    if sys_chan and sys_chan.permissions_for(ctx.guild.me).send_messages:
        await sys_chan.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                            'wait while I get a refill.'.format(ctx.guild.name))
    else:
        await general.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                           'wait while I get a refill.'.format(ctx.guild.name))

    # Add server
    guild_info = { 'server_id': ctx.guild.id, 'name': ctx.guild.name }
    response = rh.add_server(guild_info)

    if response != 200:
        await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a this code to my'
                            ' owner: {0}'.format(response.status_code))
    else:
        await sys_chan.send('I\'m now in business! Time to start collecting names')

    # if users don't match guild members, add member to the database.
    user_packet = { 'server_id': ctx.guild.id, 'users': ctx.guild.members }
    response = rh.handle_users(user_packet)

    if response == 200:
        await sys_chan.send('Names have been collected, eyeglasses have been cleaned, bunnies have been killed. Carry'
                            ' on')
    elif type(response) == tuple:
        await sys_chan.send('Some names were collected, but I couldn\'t understand some of this gibberish. The '
                            'Here, I made some weird notes: {}'.format(response[1]))
