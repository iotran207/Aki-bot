import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp
class News(commands.Cog):
    config = {
        "name": "news",
        "desc": "tin mới hàng ngày từ vnexpress:)",
        "use": "news",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def news(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get('https://vnexpress.net/')
                soup = BeautifulSoup(await get.read() , 'html.parser')
                results = []
                dess = []
                for result in soup.find_all(class_ = 'title-news'):
                    results.append(result.text)
                    results.append(result.a.get('href'))
                for des in soup.find_all(class_ = 'description'):
                    dess.append(des.text)
                title = results[0]
                link = results[1]
                des = dess[1]
                await ctx.send(f'tin mới nhất hôm nay: {title}{des}\nlink: {link}')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(News(bot))
