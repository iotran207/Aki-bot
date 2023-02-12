import discord
import aiohttp
from discord.ext import commands
import json
class Dovui(commands.Cog):
    config = {
        "name": "dovui",
        "desc": "đố vui, ko vui thì thôi:)",
        "use": "dovui",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def dovui(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get('https://docs-api.jrtxtracy.repl.co/game/dovui')
                data_txt = await get.text()
                data_json = json.loads(data_txt)
                data = {}
                question = data_json['data']['question']
                option = data_json['data']['option']
                correct = data_json['data']['correct'] 
                msg = f'đây là câu hỏi của bạn: {question}'
                stt = 1
                for i in option:
                    msg += f'\n{stt}.{i}'
                    data[str(stt)] = i
                    stt += 1
                msg += '\nreply tin nhắn theo số thứ tự các đáp án để trả lời'
                send = await ctx.send(msg)
                def check(m):
                    return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                message = await self.bot.wait_for('message', check=check)
                try:
                    if data[str(message.content)] == correct:
                        await ctx.send(f'bạn đã trả lời đúng, đáp án là {correct}')
                    else:
                        await ctx.send(f'sai rồi, đáp án là {correct}')
                except Exception as e:
                    print(e)
                    await ctx.send(f'chỉ được trả lời theo số thứ tự các đáp án')
        except Exception as e:
            print(e)
            await ctx.send(f"lệnh bạn đang sử dụng đã xảy ra lỗi, hãy báo cáo về admin bằng lệnh {get_prefix()[str(ctx.message.guild.id)]['prefix']}callad, hoặc câu trả lời của bạn không phải là một con số")
async def setup(bot):
    await bot.add_cog(Dovui(bot))
