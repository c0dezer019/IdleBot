from discord.ext import commands
from discord.utils import find
from dotenv import load_dotenv
from utility.helpers import check_idle_time, filter_channels, get_user_last_message, get_messages, generate_idle_msg
import utility.request_handler as rh
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:')

    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

    await bot.change_presence(activity = discord.Game('Cops and Robbers'))


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    sys_chan = guild.system_channel

    if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
        await sys_chan.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
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
        await sys_chan.send('Names have been collected, eyeglasses have been cleaned, bunnies have been killed. Carry'
                            ' on')
    elif type(response) == tuple:
        await sys_chan.send('Some names were collected, but I couldn\'t understand some of this gibberish. The '
                            'Here, I made some weird notes: {}'.format(response[1]))


@bot.command()
async def ping(ctx, args):
    members = ctx.message.guild.members
    user = ''

    if args:
        for i, v in enumerate(members):
            if args == v.name:
                user = v
                break

        if not user:
            await ctx.channel.send(f'{args} is not a valid user or has changed their name.')

    text_channels = filter_channels(ctx.message.guild.channels)
    all_messages = await get_messages(text_channels)
    user_last_message = get_user_last_message(all_messages, user)
    time_idle = check_idle_time(user_last_message.created_at.replace(tzinfo = None))
    response = generate_idle_msg(time_idle)

    # if user has no recent activity, label as inactive.
    # if user has recent activity, update the appropriate fields in the database.

    await ctx.channel.send(f'{user.name}' + response)


@bot.command()
async def setup(ctx):
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


bot.run(TOKEN)
