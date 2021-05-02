from discord.ext import commands
from dotenv import load_dotenv
from utility.helpers import log
import discord
import logging
import traceback
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''Got idle?'''
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)
extensions = ['cogs.admin_cmds', 'cogs.dev_cmds', 'cogs.listeners', 'cogs.setup', 'cogs.user_cmds']
logger = log(logging.ERROR, 'error_log.txt')


@bot.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    logger.error(f'Error happened within {event}:\n{traceback.format_exc()}',)

    if message.guild is not None:
        await message.guild.system_channel.send('I have encountered an error but do not worry, I will alert my owner.')


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


if __name__ == '__main__':
    for cog in extensions:
        bot.load_extension(cog)

bot.run(TOKEN, bot = True, reconnect = True)
