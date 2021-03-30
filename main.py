from discord.ext import commands
from discord.utils import find
from dotenv import load_dotenv
from utility.helpers import check_idle_time, filter_channels, get_user_last_message, get_messages, generate_idle_msg
import utility.request_handler as rh
import discord
import json
import os
import requests

load_dotenv()
TOKEN = os.getenv('TOKEN')


description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

headers = { 'Content-Type': 'application/json' }

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
    guild_packet = {'server_id': guild.id, 'name': guild.name}
    response = rh.add_server(guild_packet)
    if response.status_code != 200:
        await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a complaint to my'
                            ' owner.')
    else:
        await sys_chan.send('I\'m now in business! Time to start collecting names')

    user_packet = {'server_id': guild.id, 'users': guild.members}
    response = rh.handle_users(user_packet)

    # if users don't match guild members, add member to the database.

    # if member is in database, add guild relation to member.
    # if member already has a guild relation, do nothing.
    # For each member, assign variable for user status.


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


bot.run(TOKEN)
