from discord.ext import commands
import discord


class Clear(commands.Cog):
    config = {
        "name": "clear",
        "desc": "Xoá tin nhắn trong kênh",
        "use": "clear <Số tin nhắn muốn xoá>",
        "author": "King(aki team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int):
        messages = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(messages)} messages.")


async def setup(bot):
    await bot.add_cog(Clear(bot))
