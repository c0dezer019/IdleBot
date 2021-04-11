from discord.ext import commands
from dotenv import load_dotenv
import discord
import logging
import traceback
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)
extensions = ['cogs.admin_cmds', 'cogs.error_handler', 'cogs.listeners', 'cogs.setup_tasks', 'cogs.usr_cmds']


@bot.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    logging.warning(traceback.format_exc())

    await message.guild.system_channel.send('Oh my god, {0.mention} has caused an error.'.format(message.author))


if __name__ == '__main__':
    for cog in extensions:
        bot.load_extension(cog)

bot.run(TOKEN, bot = True, reconnect = True)
