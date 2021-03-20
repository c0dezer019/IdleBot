from discord.ext import commands
from discord.utils import find
from dotenv import load_dotenv
from utility.helpers import check_idle_time, filter_channels, get_user_last_message, get_messages, generate_idle_msg
import discord
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


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
    users = guild.members

    if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
        await sys_chan.send('Hello {}! I am here to enforce the law.'.format(guild.name))
    else:
        await general.send('Hello {}! I am here to enforce the law.'.format(guild.name))


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

    await ctx.channel.send(f'{user.name}' + response)


bot.run(TOKEN)
