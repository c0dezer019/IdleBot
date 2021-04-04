from discord.ext import commands
from dotenv import load_dotenv
import cogs as c
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''A bot to enforce the rules.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)

bot.add_cog(c.AdminCommands(bot))
bot.add_cog(c.Listeners(bot))
bot.add_cog(c.Setup(bot))
bot.add_cog(c.UserCommands(bot))

bot.run(TOKEN)
