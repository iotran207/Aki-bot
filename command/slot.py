import discord
from discord.ext import commands
import random
import main
class Slot(commands.Cog):
    config = {
        "name": "slot",
        "desc": "slot",
        "use": "slot <bet>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def slot(self, ctx, arg: int = None):
        self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
        member_data = self.bot.sql.fetchone()[0]
        if arg == None:
            await ctx.send('Bạn chưa nhập số tiền muốn cược')
        elif 10 > arg:
            await ctx.send('tiền cược không được để trống và phải từ 10$ trở lên')
        elif member_data < arg:
            await ctx.send('bạn không có đủ số tiền để chơi')
        else:
            try:
                random_icon = ['🥑', '🍐', '🥭', '🍎', '🥝', '🍇']
                result = []
                for i in range(3):
                    random_result = random.choice(random_icon)
                    result.append(random_result)
                if result[0] == result[1] or result[0] == result[2] or result[1] == result[0] or result[1] == result[2] or result[2] == result[0] or result[2] == result[1] or result[1] == result[2] == result[0]:
                    await ctx.send(f'Kết quả\n\n🕹️{result[0]} | {result[1]} | {result[2]}🕹️\n\nBạn đã thắng!')
                    await main.update(ctx.message.author.id, arg, 'win_wallet')
                else:
                    await ctx.send(f'Kết quả\n\n🕹️{result[0]} | {result[1]} | {result[2]}🕹️\n\nBạn thua rồi!:(')
                    await main.update(ctx.message.author.id, arg, 'lose_wallet')
            except Exception as e:
                print(e)
                await ctx.send('hiện tại lệnh bạn đang sử dụng đã gặp lỗi, hãy thử lại sau. xin lỗi vì sự cố này')
async def setup(bot):
    await bot.add_cog(Slot(bot))
