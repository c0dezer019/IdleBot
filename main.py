from discord.ext import commands
from dotenv import load_dotenv

from cogs import AdminCommands, Listeners, Setup, UserCommands
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)

bot.add_cog(AdminCommands(bot))
bot.add_cog(Listeners(bot))
bot.add_cog(Setup(bot))
bot.add_cog(UserCommands(bot))

bot.run(TOKEN)
