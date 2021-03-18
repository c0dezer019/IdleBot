from datetime import timezone
from discord.ext import commands
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


@bot.command()
async def status(ctx, args):
    members = ctx.message.guild.members
    user = ''

    for i, v in enumerate(members):
        if args == v.name:
            user = v
            user_id = v.id
            break

    if not user:
        await ctx.channel.send(f'{args} is not a valid user or has changed their name.')

    text_channels = filter_channels(ctx.message.guild.channels)
    all_messages = await get_messages(text_channels)
    user_last_message = get_user_last_message(all_messages, user)
    time_idle = check_idle_time(user_last_message.created_at.replace(tzinfo = None))
    response = generate_idle_msg(time_idle, user)

    await ctx.channel.send(f'{user.name}' + response)


bot.run(TOKEN)
