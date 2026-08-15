# Standard modules
import asyncio
import logging
import os
import traceback
from logging.handlers import RotatingFileHandler

# Third party modules
from dotenv import load_dotenv
from nextcord import Game, Intents
from nextcord.ext.commands import Bot
from redis.exceptions import ConnectionError, RedisError

# Internal modules
from utility.redis import AsyncRedisManager

load_dotenv()
TOKEN = os.getenv("TOKEN")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

redis = AsyncRedisManager().client

description = """Got idle? Have no more"""
intents = Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True

bot = Bot(description=description, intents=intents, command_prefix="?")

extensions = [
    "cogs.admin_cmds",
    "cogs.dev_cmds",
    "cogs.listeners",
    "cogs.setup",
    "cogs.user_cmds",
]
ignore_list: tuple = ("?ping", "?reset", "?check")
logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    global redis

    if redis is None:
        redis = AsyncRedisManager().client

    while True:
        try:
            if await redis.ping():
                logger.info("Redis successfully connected.")
                break
        except ConnectionError as e:
            logger.error("Cannot connect to Redis: %s", e)
        except RedisError as e:
            logger.error("Connect connect to Redis: %s", e)

        await asyncio.sleep(5)

    await bot.sync_application_commands()

    print(f"{bot.user} is connected to the following guilds:")

    for guild in bot.guilds:
        health = (
            "\033[32mOK\033[0m"
            if await redis.exists(f"guild:{guild.id}:meta")
            else "\033[31mX\033[0m"
        )

        print(
            f"\033[4;35m{guild.name}\033[0m (id: \033[1;34m{guild.id}\033[0m), \033[32mhealth:\033[0m {health}"
        )

    await bot.change_presence(activity=Game("Cops and Robbers"))

    if DEV_MODE and not getattr(bot, "_hot_reload_task", None):
        # on_ready can fire again on reconnect; only start the watcher once.
        from utility.hot_reload import watch_cogs

        bot._hot_reload_task = asyncio.create_task(watch_cogs(bot))
        logger.info("DEV_MODE enabled: cog hot reload active.")


@bot.event
async def on_error(event, *args, **kwargs):
    if args:
        ctx = args[0]

        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.guild.system_channel.send(
                "I have encountered an error but do not worry, I will alert my owner."
            )
    logger.error(f"Error happened within {event}: {traceback.format_exc()}")


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("bot_log.txt", maxBytes=500000, backupCount=5)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for cog in extensions:
        bot.load_extension(cog)

    bot.run(TOKEN, reconnect=True)
