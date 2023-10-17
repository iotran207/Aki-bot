import discord
from discord.ext import commands
import random
import json
import asyncio
import main as main
class Taixiu(commands.Cog):
    config = {
        "name": "taixiu",
        "desc": "Chơi tài xỉu trên discord:)",
        "use": "taixiu [tài/xỉu] <bet>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def taixiu(self, ctx, choose = None, bet = None):
        await ctx.defer()
        try:
            self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
            money = self.bot.sql.fetchone()[0]
            if int(money) < int(bet):
                await ctx.send('không đủ tiền để chơi:)')
            else:
                try:
                    dice = [random.randint(1,6), random.randint(1,6), random.randint(1,6)]
                    total = dice[0] + dice[1] + dice[2]
                    if total <= 10:
                        result = "xỉu"
                    else:
                        result = "tài"
                    list_dice2 = "⚀ ⚁ ⚂ ⚃ ⚄ ⚅".split(" ")
                    for i in range(len(dice)):
                        if dice[i-1] == 1:
                            dice[i-1] = list_dice2[0]
                        elif dice[i-1] == 2:
                            dice[i-1] = list_dice2[1]
                        elif dice[i-1] == 3:
                            dice[i-1] = list_dice2[2]
                        elif dice[i-1] == 4:
                            dice[i-1] = list_dice2[3]
                        elif dice[i-1] == 5:
                            dice [i-1] = list_dice2[4]
                        else:
                            dice[i-1] = list_dice2[5]
                    if choose == None:
                        await ctx.send('hãy cược tài hoặc xỉu')
                    elif bet == None or int(bet) < 50:
                        await ctx.send('số tiền cược không cược để trống và phải từ 50$ trở lên')
                    elif choose == result:
                        gif = 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g'
                        gif2 = 'https://media1.giphy.com/media/g9582DNuQppxC/giphy.gif?cid=ecf05e4743jop5ctofl2a5763ih04tc5b91dfnor287cu5tv&rid=giphy.gif&ct=g'
                        em_load = discord.Embed(colour = ctx.author.color, description = 'đang lắc xúc sắc...')
                        em_load.set_image(url = gif)
                        em_win = discord.Embed(colour = ctx.author.color, description = f'_Bạn đã thắng, kết quả là:_\n{dice[0]} {dice[1]} {dice[2]} | {result} và gom về được {bet}$ tiền cược')
                        em_win.set_image(url = gif2)
                        send = await ctx.send(embed = em_load)
                        await asyncio.sleep(3)
                        await send.edit(embed=em_win)
                        await main.update(ctx.message.author.id, bet, 'win_wallet')
                    elif choose != result:
                        gif = 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g'
                        gif2 = 'https://media3.giphy.com/media/l22ysLe54hZP0wubek/giphy.gif?cid=ecf05e47mba9xtd5rurzzo1flalwaqu6znpuld9vm6b2rz13&rid=giphy.gif&ct=g'
                        em_load = discord.Embed(colour = ctx.author.color, description = 'đang lắc xúc sắc...')
                        em_load.set_image(url = gif)
                        em_win = discord.Embed(colour = ctx.author.color, description = f'_bạn đã thua, kết quả là:_\n{dice[0]} {dice[1]} {dice[2]} | {result} và mất {bet}$ tiền cược')
                        em_win.set_image(url = gif2)
                        send = await ctx.send(embed = em_load)
                        await asyncio.sleep(3)
                        await send.edit(embed = em_win)
                        await main.update(ctx.message.author.id, bet, 'lose_wallet')
                    else:
                        await ctx.send('lỗi')
                except Exception as e:
                    print(e)
                    await ctx.send('error')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Taixiu(bot))
