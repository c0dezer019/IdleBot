from discord import Guild
from discord.ext.commands import Bot, Cog, bot_has_guild_permissions
from discord.utils import find

import utility.request_handler as rh


class Setup(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        sys_chan = guild.system_channel

        if sys_chan and sys_chan.permissions_for(guild.me).send_messages:
            await sys_chan.send(
                'Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                'wait while I get a refill.'.format(guild.name))
        else:
            await general.send('Hello {}! I am here to take names and drink coffee, but I am all out of coffee. Please '
                               'wait while I get a refill.'.format(guild.name))

    @Cog.listener('on_guild_join')
    @bot_has_guild_permissions(administrator = True)
    async def setup(self, guild: Guild):
        sys_chan = guild.system_channel

        # Add guild
        guild_info = { 'guild_id': guild.id, 'name': guild.name }
        response = rh.add_guild(guild_info)

        if response.status_code != 200:
            await sys_chan.send('I couldn\'t find any coffee. I no workee without coffee. Please pass a this code to my'
                                ' owner: {0}'.format(response.status_code))
        else:
            await sys_chan.send('I\'m now in business! Time to start collecting names')

        # Add members
        response = rh.add_member(guild.id, guild.members)

        if response == 200:
            await sys_chan.send(
                'Names have been collected, eyeglasses have been cleaned, and bunnies have been killed. Carry on')


def setup(bot):
    bot.add_cog(Setup(bot))
