import discord
from discord.ext import commands
import aiohttp
import json
import random
import asyncio
import aiofiles
import os
import easy_pil
class Vuatiengviet(commands.Cog):
    config = {
        "name": "vuatiengviet",
        "desc": "Game show vua tiếng việt trên discord:)",
        "use": "vuatiengviet",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vuatiengviet(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://raw.githubusercontent.com/undertheseanlp/dictionary/master/dictionary/words.txt') as word:
                    list_word = []
                    word = await word.text()
                    word = word.split('\n')
                    for i in word:
                        try:
                            text = json.loads(i)['text']
                            if len(text.split(' ')) == 2:
                                list_word.append(text)
                        except:
                            continue
                    word = random.choice(list_word).strip('-')
                    print(word)
                    text = ""
                    question = list(word.replace(" ", ""))
                    random.shuffle(question)
                    for i in question:
                        text += i+" /"
                    img = easy_pil.Editor(os.path.dirname(__file__)+'/cache/'+"vuatiengviet_background.jpg")
                    img.resize((1080,832))
                    img.text(position = (540, 680), text = text,font = easy_pil.font.Font.montserrat(variant='bold',size=30),align="center")
                    send = await ctx.send('đây là câu hỏi của bạn\nreply tin nhắn này để trả lời câu hỏi, bạn có 45 giây để trả lời', file = discord.File(img.image_bytes, filename='vuatiengviet.png'))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                    try:
                        message = await self.bot.wait_for("message", timeout=45, check=check)
                        if message: 
                            if str(message.content).lower() == word.lower():
                                await ctx.send(f"ban da tra loi dung, dap an la: '{word}'")
                            else:
                                await ctx.send(f'sai roi, dap an la "{word}"')
                    except asyncio.TimeoutError:
                        await ctx.send("hết giờ!")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Vuatiengviet(bot))