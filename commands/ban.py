import discord
from discord.ext import commands


class Ban(commands.Cog):
    config = {
        "name": "ban",
        "desc": "ban member",
        "use": "ban @mention <reason>",
        "author": "Anh Duc(aki team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member}.")


async def setup(bot):
    await bot.add_cog(Ban(bot))
