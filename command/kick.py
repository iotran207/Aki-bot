import discord
from discord.ext import commands


class Kick(commands.Cog):
    config = {
        "name": "kick",
        "desc": "ban member",
        "use": "kick @mention <reason>",
        "author": "Anh Duc(aki team)"
    }

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member}.")


async def setup(bot):
    await bot.add_cog(Kick(bot))
