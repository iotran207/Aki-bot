import discord
from discord.ext import commands
import aiohttp
from command.cache.list_color import list_color
import random
import json
class Translate(commands.Cog):
    config = {
        'name': "translate",
        "desc": "Google dịch=)",
        "use": "translate <text>\n<prefix>translate {reply message}",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def translate(self, ctx, *,text=None):
        try:
            if not text and not ctx.message.reference:
                await ctx.send("error: Bạn chưa nhập văn bản cần dịch")
            else:
                    if ctx.message.reference:
                        text = ctx.message.reference.resolved.content
                        async with aiohttp.ClientSession() as session:
                            r = await session.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=vi&dt=t&q={text}")
                            data = json.loads(await r.text())
                            trans = ""
                            for i in data[0]:
                                trans += i[0]
                            em = discord.Embed(title="**Google Translate**", description = f"_{trans}_", color=random.choice(list_color))
                            em.set_footer(text=f"translated {data[8][0][0]} -> vi")
                            em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                            await ctx.send(embed=em)
                    else:
                        async with aiohttp.ClientSession() as session:
                            r = await session.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=vi&dt=t&q={text}")
                            data = json.loads(await r.text())
                            trans = ""
                            for i in data[0]:
                                trans += i[0]
                            em = discord.Embed(title="**Google Translate**", description = f"_{trans}_", color=random.choice(list_color))
                            em.set_footer(text=f"translated {data[8][0][0]} -> vi")
                            em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                            await ctx.send(embed=em)
        except Exception as e:
            print
async def setup(bot):
    await bot.add_cog(Translate(bot))
        
