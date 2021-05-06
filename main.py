from discord import Game
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from typing import Dict
import arrow
import discord
import logging
import os
import utility.request_handler as rh

load_dotenv()
TOKEN = os.getenv('TOKEN')

description = '''Got idle?'''
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix = '?', description = description, intents = intents)
extensions = ['cogs.admin_cmds', 'cogs.dev_cmds', 'cogs.setup', 'cogs.user_cmds']
ignore_list: tuple = ('?ping', '?reset', '?check')

logger = logging.getLogger('IdleBot Logger')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler(f'bot_log.txt', maxBytes = 500000, backupCount = 5)
logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


@bot.event
async def on_ready(self):
    print(f'{bot.user} is connected to the following guilds:')

    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

    await bot.change_presence(activity = Game('Cops and Robbers'))


@bot.event
async def on_member_join(member: discord.Member):
    chan_index: int = bot.guilds.index(member.guild)

    general: discord.TextChannel = get(member.guild.channels, name = 'general')
    sys_chan: discord.TextChannel = member.guild.system_channel

    if sys_chan and sys_chan.permissions_for(bot.guilds[chan_index].me).send_messages:
        await sys_chan.send('Welcome {0.mention}!'.format(member))
    else:
        await general.send('Welcome {0.mention}!'.format(member))

    try:
        rh.add_member(member.guild.id, member)

    except Exception:
        raise


@bot.event
async def on_message(message: discord.Message):
    if message.guild is not None:
        if message.content.startswith(ignore_list):
            return

        member_id = message.author.id
        guild_id = message.author.guild.id
        data_to_change = {
            'last_activity': message.channel.type[0],
            'last_activity_loc': message.channel.name,
            'last_activity_ts': arrow.now('US/Central').isoformat(),
            'status': 'active',
        }

        if not message.author.bot:
            try:
                rh.update_member(member_id, **data_to_change)
                rh.update_guild(guild_id, **data_to_change)

            except AttributeError:
                raise

            except TypeError:
                raise

            except ValueError:
                raise

    elif not message.guild and str(message.channel.type) == 'private' and not message.author.bot:
        await message.channel.send(
            'Sorry, but I do not respond to DM\'s other than with this message. Try using me in a guild '
            'that I am in.')


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    try:
        if before.nick != after.nick:
            rh.update_member(after.id, **{ 'nickname': after.nick })
        else:
            pass

    except AttributeError:
        raise


@bot.event
async def on_user_update(before: discord.User, after: discord.User):
    try:
        if before.name != after.name or before.discriminator != after.discriminator:
            username = f'{after.name}#{after.discriminator}'

            rh.update_member(after.id, **{ 'username': username })
        else:
            pass

    except Exception:
        raise


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    try:
        payload: Dict = {
            'last_activity': 'voice',
            'last_activity_loc': str(after.channel),
            'last_activity_ts': arrow.now('US/Central').isoformat()
        }

        rh.update_member(member.id, **payload)
        rh.update_guild(member.guild.id, **payload)

    except Exception:
        raise


@bot.event
async def on_guild_update(before: discord.Guild, after: discord.Guild):
    try:
        if before.name != after.name:
            rh.update_guild(after.id, **{ 'name': after.name })
        else:
            pass
    except Exception:
        raise


@bot.event
async def on_error(event, *args, **kwargs):
    if len(args) > 0:
        message = args[0]

        if message.guild is not None:
            await message.guild.system_channel.send(
                'I have encountered an error but do not worry, I will alert my owner.')


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


if __name__ == '__main__':
    for cog in extensions:
        bot.load_extension(cog)

bot.run(TOKEN, bot = True, reconnect = True)
