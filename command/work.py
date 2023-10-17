import random
import discord
from discord.ext import commands
class Work(commands.Cog):
    config = {
        "name": "work",
        "desc": "Có làm thì mới có ăn",
        "use": "work",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        try:
            send = await ctx.send('đây là các việc bạn có thể làm để kiếm tiền\n1. Bán vé số\n2. Sửa xe\n3. Lập trình viên\n4. Thợ hồ\n5. Bán hàng online\n6. Sưu tầm code hent cho admin bot:)))\nreply tin nhắn theo số thứ tự để chọn việc muốn làm')
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
            message = await self.bot.wait_for('message', check = check, timeout=45)
            earn = random.randint(50, 350)
            rd_sx = ['trộm ốc xe của khách đem bán:)', "", "được khách giàu mua gói bảo dưỡng toàn phần", "đem mấy tấm nhôm, sắt thừa của xe đi bán đồng nát"]
            rd_lt = ["code app dự báo thời tiết", "code module bot aki-chan đem bán:))", "code web hen=)"]
            if message.content.lower() == '1':
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn đi bán vé số và kiếm được {earn}$")
            elif str(message.content).lower() == '2':
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn làm thợ sửa xe, {random.choice(rd_sx)} kiếm được {earn}$")
            elif str(message.content).lower() == '3':
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn làm lập trình viên {random.choice(rd_lt)} kiếm được {earn}$")
            elif str(message.content).lower() == "4":
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn làm phụ hồ kiếm được {earn}$")
            elif str(message.content).lower() == "5":
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn đi bán hàng online chốt {random.randint(5, 30)} đơn đồng giá 1k shopee kiếm được {earn}=))")
            elif str(message.content) == "6":
                self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
                await ctx.send(f"Bạn được nhiều code hơn chất lượng cho admin nên được thưởng {earn}$, ib admin share link full nhé=))")
            self.bot.database.commit()
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Work(bot))
