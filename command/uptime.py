from discord.ext import commands
import discord


class Uptime(commands.Cog):
    config = {
        "name": "uptime",
        "desc": "kiểm tra thời gian online của bot",
        "use": "uptime",
        "author": "King.(maku team)"
    }

    def __init__(self, bot):
        self.bot = bot

        self.START_TIME = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.START_TIME = discord.utils.utcnow()

    @commands.command()
    async def uptime(self, ctx):
        em = discord.Embed(
            title='UPTIME',
            color=0xFFFFF
        ).add_field(
            name='<:uptime:1014548798728577085> Uptime',
            value=f'┕{discord.utils.format_dt(self.START_TIME, "F")}',
            inline=True
        ).add_field(
            name='<:tixung4:1014550478161448990> Active servers',
            value=f'┕ {str(len(self.bot.guilds))} servers',
            inline=True
        ).add_field(
            name='<:hehe:1014195246554427442> Active users',
            value=f'┕{str(len(self.bot.users))} users',
            inline=True
        )
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Uptime(bot))
