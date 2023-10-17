from discord.ext import commands
import discord
from command.cache.list_color import list_color
import random
class Totinh(commands.Cog):
    config = {
        "name": "totinh",
        "desc": "tỏ tình người bạn thích",
        "use": "totinh <id người bạn thích> <lời tỏ tình>",
        "author": "King.(maku team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.dm_only()
    async def totinh(self,ctx):
        await ctx.send('Bạn muốn gửi lời tỏ tình này đến ai nào(id người ấy)! Tớ sẽ gửi tin nhắn cho bạn ấy dưới dạng ẩn danh nên cậu không phải lo đâu😳')
        member_message = await self.bot.wait_for('message')
        await ctx.send('Nhập lời tỏ tình của bạn zô đây nè😘!')
        message = await self.bot.wait_for('message')
        get_user = await self.bot.fetch_user(member_message.content)
        await ctx.send('Ting tớ gửi lời chúc đến ng đó rồi nhen :3😘!')
        em = discord.Embed(title='ting! ting! Bạn có 1 lời tỏ tình từ ẩn danh',description=f"lời nhắn đó là:{message.content}",color=random.choice(list_color))
        em.set_image(url='https://media.giphy.com/media/26FLdmIp6wJr91JAI/giphy.gif')
        await get_user.send(embed=em)


async def setup(bot):
    await bot.add_cog(Totinh(bot))
