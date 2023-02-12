from discord.ext import commands
import discord


class Avatar(commands.Cog):
    config = {
        "name": "avatar",
        "desc": "avatar của member trong server",
        "use": "avatar [@mention]",
        "author": "Anh Duc(aki team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member=None):
        member = member or ctx.author

        await ctx.reply(member.display_avatar)


async def setup(bot):
    await bot.add_cog(Avatar(bot))
