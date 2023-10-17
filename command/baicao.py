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
    @commands.hybrid_command()
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
            await open_account(ctx.message.guild.id)
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
            elif arg == 'bot':
                if arg2 == None:
                    return await ctx.send("Ban chua dat tien cuoc")
                bot = 1
                user = 1
                user_cards = []
                bot_cards=[]
                for i in range(2):
                    card1 = random.randint(1, 10)
                    card2 = random.randint(1, 10)
                    card3 = random.randint(1, 10)
                    result = card1+card2+card3
                    if result >= 10:
                        result -= 10
                    if result >= 10:
                        result -= 10
                    if result >= 10:
                        result -= 10
                    if i:
                        bot = result
                        bot_cards= [card1,card2,card3]
                    else:
                        user = result
                        user_cards=[card1,card2,card3]
                msg = f"Bot[?]:\n ? | ? | ? |\nBạn[{user}]:\n{user_cards[0]} | {user_cards[1]} | {user_cards[2]}"
                
                em = discord.Embed(title="**CASINO**",description=f"{msg}",color  = discord.Color.green())
                em.set_footer(text = "Xuất hiện kết quả sau 5s")
                em.set_image(url= 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g')
                em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                message= await ctx.send(embed=em)
                await asyncio.sleep(5)
                
                msg = f"Bot[{bot}]:\n {bot_cards[0]} | {bot_cards[1]} | {bot_cards[2]} |\nBạn[{user}]:\n{user_cards[0]} | {user_cards[1]} | {user_cards[2]}"
                
                em = discord.Embed(title="**CASINO**",description=f"{msg}",color  = discord.Color.green())
                em.set_image(url= 'https://media1.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif?cid=ecf05e47venaa45nhe4pmfsckgtrjasrpdzs6vtmpvwya6fk&rid=giphy.gif&ct=g')
                em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                arg2 = int(arg2)
                if  bot > user:
                    await update(ctx.author.id, int(arg2), 'lose_wallet')
                    em.set_footer(text = f"Bạn đã thua {arg2}$")
                elif user > bot:
                    await update(ctx.author.id, int(arg2), 'win_wallet')
                    em.set_footer(text = f"Bạn đã thắng {arg2}$")
                else:
                    em.set_footer(text = f"Hoà")
                await message.edit(embed=em)
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
                    em = discord.Embed(title = "**CASINO**",description=f'**đã chia bài thành công, bot sẽ thông báo kết quả sau 25 giây nữa**',color=discord.Color.green())
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
