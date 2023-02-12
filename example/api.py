from discord.ext import commands
import discord
import aiohttp #sử dụng aiohttp thay cho requests 
class Demo2(commands.Cog):
    config = {
        "name": "...", #tên lệnh
        "desc": "...", #mô tả về lệnh
        "use": "...", #cách sử dụng 
        "author": "...", #credit tác giả
        "event": False #nếu là event thì để True còn là lệnh thì để False hoặc không để gì cũng đc:))
    }
    def __init__(self, bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession()
    @commands.command()
    async def simimi(self,ctx,*,content:str):
        async with self.bot.session.get(f'https://docs-api.nguyenhaidang.ml/sim?type=ask&ask={content}') as get_answer: #gửi request đến api (có thể đọc docs của aiohttp để biết rõ hơn-))
            answer = await get_answer.json()
            await ctx.reply(answer['answer'])
    


async def setup(bot):
    await bot.add_cog(Demo2(bot))
