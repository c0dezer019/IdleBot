from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)
extensions = ['cogs.admin_cmds', 'cogs.setup_tasks', 'cogs.usr_cmds']

if __name__ == '__main__':
    for cog in extensions:
        bot.load_extension(cog)

bot.run(TOKEN, bot = True, reconnect = True)
