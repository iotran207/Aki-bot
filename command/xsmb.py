import discord
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from discord.ext import commands


class Xsmb(commands.Cog):
    config = {
        "name": "xsmb",
        "desc": "kết quả xổ số miền bắc",
        "use": "xsmb",
        "author": "Anh Duc(aki team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xsmb(self, ctx):
        # xsmb
        try:
            result = []
            url = 'https://www.xoso.net/getkqxs/mien-bac.js'
            async with aiohttp.ClientSession() as session:
                get_data = await session.get(url)
                x = await get_data.text()
                soup = BeautifulSoup(x, 'html.parser')
                for a in soup.find_all(class_='giaidb'):
                    result.append(a.text)
                for c in soup.find_all(class_='giai1'):
                    result.append(c.text)
                for d in soup.find_all(class_='giai2'):
                    result.append(d.text)
                for e in soup.find_all(class_='giai3'):
                    result.append(e.text)
                for f in soup.find_all(class_='giai4'):
                    result.append(f.text)
                for g in soup.find_all(class_='giai5'):
                    result.append(g.text)
                for h in soup.find_all(class_='giai6'):
                    result.append(h.text)
                for k in soup.find_all(class_='giai7'):
                    result.append(k.text)
                for l in soup.find_all(class_='ngay'):
                    result.append(l.text)
                t = '\t'
                n = '\n'
                await ctx.send(
                    f'Kết quả xổ số miền Bắc {str(result[8]).strip(f"{t}")}{n}{n}Giải đặc biệt: {str(result[0]).strip(f"{t}")}{n}Giải nhất: {str(result[1]).strip(f"{t}")}{n}Giải nhì: {str(result[2]).strip(f"{t}")}{n}Giải ba: {str(result[3]).strip(f"{t}")}\nGiải tư: {str(result[4]).strip(f"{t}")}{n}Giải năm: {str(result[5]).strip(f"{t}")}{n}Giải sáu: {str(result[6]).strip(f"{t}")}{n}Giải bảy: {str(result[7]).strip(f"{t}")}')
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Xsmb(bot))
