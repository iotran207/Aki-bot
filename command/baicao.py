import discord
from discord.ext import commands
import json
from main import config, save_member_data, open_account, get_bank_data, update
import random
import asyncio
class Baicao(commands.Cog):
    config = {
        "name": "baicao",
        "desc": "Choi bai cao tren discord:)))",
        "use": "baicao [create/start/join/leave]",
        "author": "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baicao(self, ctx, arg = None, arg2 = None):
        try:
            def natural_keys(text):
                return text.split(":")[1]
            def read():
                with open(r"command/data.json", 'r') as f:
                    users = json.load(f)
                    return users
            def save(data):
                save_member_data(data)
            await open_account(ctx.message.author.id)
            self.bot.sql.execute(f'SELECT user_money FROM user_data WHERE user_id={ctx.author.id}')
            money = self.bot.sql.fetchone()[0]
            money_data = await get_bank_data()
            users = read()
            list_player_result = []
            message = ""
            prefix = config["prefix"]
            if arg == None:
                await ctx.send(f'game bài cào nhiều người chơi\n{prefix}baicao [create/start/join/leave]')
            elif arg == 'create':
                if arg2 == None or int(arg2) < 50:
                    await ctx.send(f'bạn chưa nhập số tiền muốn cược cho bàn chơi hoặc số tiền bạn muốn cược nhỏ hơn 50$')
                elif int(arg2) > int(money):
                    await ctx.send(f'bạn không đủ số tiền để chơi')
                elif 'baicao' in users[str(ctx.message.guild.id)]:
                    await ctx.send(f'đã có một bàn bài cào được tạo trước đó, không thể tạo thêm')
                else:
                    users[str(ctx.message.guild.id)] = {}
                    users[str(ctx.message.guild.id)]['baicao'] = {}
                    users[str(ctx.message.guild.id)]['baicao']['baicao_create'] = True
                    users[str(ctx.message.guild.id)]['baicao']['player'] = [str(ctx.message.author.id)]
                    users[str(ctx.message.guild.id)]['baicao']['player_name'] = [str(ctx.message.author)]
                    users[str(ctx.message.guild.id)]['baicao']['author'] = str(ctx.message.author.id)
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)] = {}
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)]['change'] = 2
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)]['result'] = None
                    users[str(ctx.message.guild.id)]['baicao']['bet'] = int(arg2)
                    print(users)
                    save_member_data(users)
                    em = discord.Embed(description=f"Đã tạo bàn bài cào thành công\nHãy nhập {prefix}baicao join để tham gia bàn chơi (người tạo không cần nhập)")
                    await ctx.reply(embed = em)
            elif arg == 'join':
                if 'baicao' not in users[str(ctx.message.guild.id)]:
                    await ctx.reply('chưa tạo bàn bài cào để tham gia bàn chơi')
                elif len(users[str(ctx.message.guild.id)]['baicao']['player']) == 4:
                    await ctx.reply('số người chơi tối đa là 4 người')
                elif str(ctx.message.author.id) in users[str(ctx.message.guild.id)]['baicao']['player'] or str(ctx.message.author.id) in users[str(ctx.message.guild.id)]['baicao']['player_name']:
                    await ctx.reply('bạn đã tham gia bàn choi, không thể tham gia lại')
                elif users[str(ctx.message.guild.id)]['baicao']['bet'] > money:
                    await ctx.reply(f'bạn không đủ số tiền để chơi')
                else:
                    users[str(ctx.message.guild.id)]['baicao']['player'].append(str(ctx.message.author.id))
                    users[str(ctx.message.guild.id)]['baicao']['player_name'].append(str(ctx.message.author))
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)] = {}
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)]['change'] = 2
                    users[str(ctx.message.guild.id)]['baicao'][str(ctx.message.author)]['result'] = None
                    save(users)
                    await ctx.reply("đã tham gia bàn chơi")
            elif arg == 'leave':
                    if str(ctx.message.author.id) != users[str(ctx.message.guild.id)]['baicao']['author']:
                       users[str(ctx.message.guild.id)]['baicao']['player'].remove(str(ctx.message.author.id))
                       users[str(ctx.message.guild.id)]['baicao']['player_name'].remove(str(ctx.message.author))
                       save(users)
                       await ctx.send(f'{ctx.message.author.name} đã rời bàn chơi')
                    else:
                        del users[str(ctx.message.guild.id)]['baicao']
                        save(users)
                        await ctx.send('chủ bàn đã hủy bàn chơi, hãy tạo một bàn chơi khác để tiếp tục')
            elif arg == 'start':
                list_player_id = []
                if 'baicao' not in users[str(ctx.message.guild.id)]: 
                    await ctx.send('chưa tạo bàn bài cào để bắt đầu')
                elif len(users[str(ctx.message.guild.id)]['baicao']['player']) < 2: 
                    await ctx.send('cần ít nhất 2 người trong bàn chơi để bắt đầu')
                else:   
                    for i in range(len(users[str(ctx.message.guild.id)]['baicao']['player'])):
                        card1 = random.randint(1, 9)
                        card2 = random.randint(1, 9)
                        card3 = random.randint(1, 9)
                        result = card1 + card2 + card3
                        if result >= 10:
                            result -= 10
                        if result >= 10:
                            result -= 10
                        user = await self.bot.fetch_user(str(users[str(ctx.message.guild.id)]['baicao']['player'][i - 1]))
                        await update(str(user.id), users[str(ctx.message.guild.id)]['baicao']['bet'], 'lose_wallet')
                        list_player_result.append(f"{user.name}: {result}")
                        list_player_id.append(f"{user.id}: {result}")
                        await user.send(f"bài của bạn: {card1} | {card2} | {card3}\ntổng bài: {result}")
                    list_player_result.sort(key =natural_keys, reverse=True)
                    list_player_id.sort(key =natural_keys, reverse=True)
                    print(list_player_result)
                    
                    rank = 1
                    player_win_id = list_player_id[0].split(":")[0]
                    player_win_info = await self.bot.fetch_user(str(player_win_id))
                    player_win_name = player_win_info.name
                    win_bet = int(users[str(ctx.message.guild.id)]['baicao']['bet']) * int(len(users[str(ctx.message.guild.id)]['baicao']['player']))
                    users[str(ctx.message.guild.id)]['baicao']['baicao_start'] = True
                    save(users)
                    em = discord.Embed(description=f'**đã chia bài thành công, bot sẽ thông báo kết quả sau 25 giây nữa**')
                    await ctx.send(embed = em)
                    await asyncio.sleep(25)
                    for k in list_player_result:
                        message = message + f"**{rank}. {k}**\n"
                        rank += 1
                    message = message + f"\n**{player_win_name} là người chiến thắng và gom về {win_bet}$ tiền cược**"
                    await update(player_win_id, int(win_bet), 'win_wallet')
                    em = discord.Embed(title= "**Kết Quả**", description=message)
                    await ctx.send(embed=em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Baicao(bot))