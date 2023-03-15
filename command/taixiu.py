import discord
from discord.ext import commands
import aiohttp
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
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def taixiu(self, ctx, arg1 = None, arg2 = None):
        try:
            self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
            money = self.bot.sql.fetchone()[0]
            if int(money) < int(arg2):
                await ctx.send('không đủ tiền để chơi:)')
            else:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get('https://api.hclaptrinh.repl.co/api/taixiu') as resp:
                            data_json = json.loads(await resp.text())
                    result = data_json['result']
                    dice = data_json['dice']
                    list_dice = ['<:dice1:986218979662118912>', '<:dice2:986218949064654899>', '<:dice3:986218921344503818>', '<:dice4:986218884526911589>', '<:dice5:986218782324326410>', '<:dice6:986218835352879135>']
                    for i in range(len(dice)):
                        if dice[i-1] == 1:
                            dice[i-1] = list_dice[0]
                        elif dice[i-1] == 2:
                            dice[i-1] = list_dice[1]
                        elif dice[i-1] == 3:
                            dice[i-1] = list_dice[2]
                        elif dice[i-1] == 4:
                            dice[i-1] = list_dice[3]
                        elif dice[i-1] == 5:
                            dice [i-1] = list_dice[4]
                        else:
                            dice[i-1] = list_dice[5]
                    if result == 'xiu':
                        result = 'xỉu'
                    elif result == 'tai':
                        result = 'tài'
                    if arg1 == None:
                        await ctx.send('hãy cược tài hoặc xỉu')
                    elif arg2 == None or int(arg2) < 50:
                        await ctx.send('số tiền cược không cược để trống và phải từ 50$ trở lên')
                    elif arg1 == result:
                        gif = 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g'
                        gif2 = 'https://media1.giphy.com/media/g9582DNuQppxC/giphy.gif?cid=ecf05e4743jop5ctofl2a5763ih04tc5b91dfnor287cu5tv&rid=giphy.gif&ct=g'
                        em_load = discord.Embed(colour = ctx.author.color, description = 'đang lắc xúc sắc...')
                        em_load.set_image(url = gif)
                        em_win = discord.Embed(colour = ctx.author.color, description = f'_Bạn đã thắng, kết quả là:_\n{dice[0]} {dice[1]} {dice[2]} | {result} và gom về được {arg2}$ tiền cược')
                        em_win.set_image(url = gif2)
                        send = await ctx.send(embed = em_load)
                        await asyncio.sleep(3)
                        await send.edit(embed=em_win)
                        await main.update(ctx.message.author.id, arg2, 'win_wallet')
                    elif arg1 != result:
                        gif = 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g'
                        gif2 = 'https://media3.giphy.com/media/l22ysLe54hZP0wubek/giphy.gif?cid=ecf05e47mba9xtd5rurzzo1flalwaqu6znpuld9vm6b2rz13&rid=giphy.gif&ct=g'
                        em_load = discord.Embed(colour = ctx.author.color, description = 'đang lắc xúc sắc...')
                        em_load.set_image(url = gif)
                        em_win = discord.Embed(colour = ctx.author.color, description = f'_bạn đã thua, kết quả là:_\n{dice[0]} {dice[1]} {dice[2]} | {result} và mất {arg2}$ tiền cược')
                        em_win.set_image(url = gif2)
                        send = await ctx.send(embed = em_load)
                        await asyncio.sleep(3)
                        await send.edit(embed = em_win)
                        await main.update(ctx.message.author.id, arg2, 'lose_wallet')
                    else:
                        await ctx.send('lỗi')
                except Exception as e:
                    print(e)
                    await ctx.send('error')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Taixiu(bot))
