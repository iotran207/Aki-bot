import discord
from discord.ext import commands
from main import update
class Bank(commands.Cog):
    config = {
        "name": "bank",
        "desc": "aki-bot bank",
        "use": "bank <-s/-d/-w> <amount> \nmode:\n-s: chuyen tien\n\n<prefix>bank -s <amount> @mention\n-d: gui tien\n-w: rut tien",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bank(self, ctx, mode=None, amount=None, member: discord.User=None):
        try:
            if mode == None:
                await ctx.send("sai cu phap")
            elif str(mode).lower()=="-w":
                self.bot.sql.execute(f'SELECT user_bank FROM user_data WHERE user_id={ctx.author.id}')
                bank = self.bot.sql.fetchone()[0]
                if amount==None or not str(amount).isdigit():
                    await ctx.send("error")
                    return
                elif int(amount) > int(bank):
                    await ctx.send("ko du tien")
                    return
                await update(ctx.author.id, amount, "win_wallet")
                await update(ctx.author.id, amount, "lose_bank")
                await ctx.send(f"Rút tiền thành công {amount}$ từ tài khoản")
            elif str(mode).lower() == "-s":
                self.bot.sql.execute(f'SELECT user_bank FROM user_data WHERE user_id={ctx.author.id}')
                bank = self.bot.sql.fetchone()[0]
                if amount == None or not str(amount).isdigit() or member == None:
                    await ctx.send("error")
                    return
                elif int(amount) > int(bank):
                    await ctx.send("khong du tien")
                    return
                member = member.id
                await update(ctx.author.id, amount, "lose_bank")
                await update(member, amount, "win_bank")
                await ctx.send(f"Chuyển tiền thành công {amount}$ cho <@{member}>")
            elif str(mode).lower() == "-d":
                self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
                money = self.bot.sql.fetchone()[0]
                if amount ==None or not str(amount).isdigit():
                    await ctx.send("error")
                    return
                elif int(amount) > int(money):
                    await ctx.send("ko du tien")
                    return
                await update(ctx.author.id, amount, "lose_wallet")
                await update(ctx.author.id, amount, "win_bank")
                await ctx.send(f"Đã bỏ {amount}$ vào tài khoản ngân hàng")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Bank(bot))
