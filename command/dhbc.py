import discord
from discord.ext import commands
import json
import aiofiles
import aiohttp
import sys
import random
import io
import main
import random
from command.cache.list_color import list_color
import aiofiles
import os
class Dhbc(commands.Cog):
    config = {
        "name": "dhbc",
        "desc": "Game đuổi hình bắt chữ",
        "use": "dhbc",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def dhbc(self, ctx):
        try:
            self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
            money = self.bot.sql.fetchone()[0]
            self.bot.sql.execute(f'SELECT user_bank FROM user_data WHERE user_id={ctx.author.id}')
            bank = self.bot.sql.fetchone()[0]
            async def wait_message(msg):
                def check(m):
                    return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                message = await self.bot.wait_for('message', check=check)
                return message
            url_DHBC = [
                'https://www.nguyenmanh.name.vn/api/dhbc1?apikey=KCL98tNB',
                "https://goatbotserver.onrender.com/api/duoihinhbatchu"
            ]
            random_dhbc = random.choice(url_DHBC)
            async with aiohttp.ClientSession() as session:
                get_DHBC = await session.get(random_dhbc)
                data_DHBC = await get_DHBC.text()
                json_DHBC = json.loads(data_DHBC)
            embed = discord.Embed(colour = random.choice(list_color), title = "===ĐUỔI HÌNH BẮT CHỮ===", description = 'đây là câu hỏi của bạn\nreply "gợi ý" nếu bạn muốn xem gợi ý cho câu hỏi(50$/lần)')
            if random_dhbc == url_DHBC[0]:
                image_DHBC = json_DHBC['result']['link']
                sokt = json_DHBC['result']['sokitu']
                dapan = json_DHBC['result']['tukhoa']
                async with aiohttp.ClientSession() as session:
                    img = await session.get(image_DHBC)
                    img = await img.read()
                    f = await aiofiles.open(os.path.dirname(__file__) + "/cache/dhbc.png", mode="wb")
                    await f.write(img)
                    await f.close()
                embed.set_image(url = "attachment://dhbc.png")
                send = await ctx.send(embed=embed,file=discord.File(os.path.dirname(__file__) + "/cache/dhbc.png", filename="dhbc.png"))
                if "a" in random_dhbc:
                    message = await wait_message(send)
                    if str(message.content.lower()) == dapan:
                        await ctx.send(f'bạn đã trả lời đúng, đáp án là: {dapan}')
                    elif str(message.content.lower()) == "gợi ý":
                        if money >= 50:
                            await main.update(ctx.author.id, 50, "lose_wallet")
                            await ctx.send(f"Gợi ý từ này là {sokt} (tiếp tục reply câu hỏi ở trên để trả lời)")
                        else:
                            await ctx.send("bạn không đủ 50$ để xem gợi ý(tiếp tục reply câu hỏi ở trên để trả lời)")
                        message = await wait_message(send)
                        if message.content.lower() == dapan:
                            await ctx.send(f'bạn đã trả lời đúng, đáp án là: {dapan}')
                        else:
                            await ctx.send(f'sai rồi, đáp án là {dapan}')
                    else:
                        await ctx.send(f'sai rồi, đáp án là {dapan}')
            elif random_dhbc == url_DHBC[1]:
                json_dhbc = json_DHBC["data"]
                img = json_dhbc["image1and2"]
                answer = json_dhbc["wordcomplete"]
                goi_y = json_dhbc["soluongkt"]
                async with aiohttp.ClientSession() as session:
                    img = await session.get(img)
                    img = await img.read()
                    f = await aiofiles.open(os.path.dirname(__file__) + "/cache/dhbc.png", mode="wb")
                    await f.write(img)
                    await f.close()
                embed.set_image(url = "attachment://dhbc.png")
                send = await ctx.send(embed=embed,file=discord.File(os.path.dirname(__file__) + "/cache/dhbc.png", filename="dhbc.png"))
                message = await wait_message(send)
                if message.content.upper() == answer:
                    await ctx.send(f'bạn đã trả lời đúng, đáp án là: {answer}')
                elif message.content.lower() == "gợi ý":
                    if money >= 50:
                        await main.update(ctx.author.id, 50, "lose_wallet")
                        await ctx.send(f"gợi ý: từ này gồm {goi_y} kí tự (tiếp tục reply câu hỏi ở trên để trả lời)")
                    else:
                        await ctx.send("bạn không đủ 50$ để xem gợi ý (tiếp tục reply câu hỏi ở trên để trả lời)")
                    message = await wait_message(send)
                    if message.content.upper() == answer:
                        await ctx.send(f"bạn đã trả lời đúng, đáp án là: {answer}")
                    else:
                        await ctx.send(f"sai rồi đáp án là {answer}")
                else:
                    await ctx.send(f"sai rồi đáp án là {answer}")
                    
        except Exception as e:
            print(e)
            await ctx.send(
                'hiện tại lệnh bạn đang sử dụng đã gặp lỗi, hãy thử lại sau. xin lỗi vì sự cố này'
            )
async def setup(bot):
    await bot.add_cog(Dhbc(bot))
