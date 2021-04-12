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
extensions = ['cogs.admin_cmds', 'cogs.listeners', 'cogs.setup_tasks', 'cogs.usr_cmds']


@bot.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    traceback.print_exc(file = 'utility/error_log')

    await message.guild.system_channel.send('I have encountered an error but do not worry, I will alert my owner.')


if __name__ == '__main__':
    for cog in extensions:
        bot.load_extension(cog)

bot.run(TOKEN, bot = True, reconnect = True)
