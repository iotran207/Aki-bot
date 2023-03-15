from discord.ext.commands import *
from discord import *
from discord.ext import commands
import discord
class Money(commands.Cog):
    try:
        config = {
            "name": "money",
            "desc": "Xem số tiền hiện có của bạn trên bot",
            "use": "money",
            "author": "King(maku team)"
        }

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_message(self, message: Message):
            self.bot.sql.execute(f'SELECT * FROM user_data WHERE user_id={message.author.id}')
            if self.bot.sql.fetchone() == None:
                self.bot.sql.execute(
                    f'INSERT INTO user_data (user_id,user_money,user_bank) VALUES ({message.author.id}, 0, 0)')

            self.bot.database.commit()

        @commands.command(aliases=["bal", "balance"])
        @commands.cooldown(1, 4, commands.BucketType.user)
        async def money(self, ctx, member: discord.User=None):
            try:
                if member==None:
                    self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
                    money = self.bot.sql.fetchone()[0]
                    self.bot.sql.execute(f'SELECT user_bank FROM user_data WHERE user_id={ctx.author.id}')
                    bank = self.bot.sql.fetchone()[0]
                    em = Embed(title=f'_Tài khoản của {ctx.author.display_name}_', color=0xFFF)
                    em.add_field(name="_💵Cash_", value=str(money) + 'VNĐ')
                    em.add_field(name="_💳Bank_", value=str(bank) + 'VNĐ')
                    await ctx.reply(embed=em)
                    return
                self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={member.id}')
                money = self.bot.sql.fetchone()[0]
                self.bot.sql.execute(f'SELECT user_bank FROM user_data WHERE user_id={member.id}')
                bank = self.bot.sql.fetchone()[0]
                em = Embed(title=f'_Tài khoản của {member.name}_', color=0xFFF)
                em.add_field(name="_💵Cash_", value=str(money) + 'VNĐ')
                em.add_field(name="_💳Bank_", value=str(bank) + 'VNĐ')
                await ctx.reply(embed=em)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
async def setup(bot):
    await bot.add_cog(Money(bot))
