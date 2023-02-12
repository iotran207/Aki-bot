from discord.ext import commands
class React_to_delete(commands.Cog):
    config = {
        "event": True
    }
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if(message.author.id == self.bot.user.id):
            await message.delete()


async def setup(bot):
    await bot.add_cog(React_to_delete(bot))