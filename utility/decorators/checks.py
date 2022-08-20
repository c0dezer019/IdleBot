from discord.ext import commands


def is_bot_developer():
    def predicate(ctx: commands.Context):
        return ctx.message.author.id == 102588778232705024

    return commands.check(predicate)

def bot_only_command():
  def predicate(ctx: commands.Context, bot: commands.Bot):
    return ctx.message.author.bot

  return commands.check(predicate)
