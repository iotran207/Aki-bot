import discord
from discord.ext import commands
import chess
from fentoboardimage import fenToImage, loadPiecesFolder
import io
import os
class Chess(commands.Cog):
    config = {
        "name": "chess",
        "desc": "chơi cờ vua+)",
        "use": "chess <@mention>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "chess")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chess(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("@mention một người để chơi cùng bạn, hoặc tự đánh một mình bằng cách @mention chính bạn=))")
        else:    
            try:
                def load_img(fen):
                    boardImage = fenToImage(
                	fen= fen,
                	squarelength=100,
                	pieceSet=loadPiecesFolder(os.path.dirname(__file__) + "/cache/chess_pieces"),
                	darkColor="#D18B47",
                	lightColor="#FFCE9E"
                )
                    bytes = io.BytesIO()
                    boardImage.save(bytes, "png")
                    bytes.seek(0)
                    return bytes
                board = chess.Board()
                send = await ctx.reply(f"ván cờ đã bắt đầu, quân trắng đi trước (lượt của <@{ctx.message.author.id}>), hãy di chuyển quân bằng cách gõ theo vị trí trên bàn cờ\nLưu ý: nếu muốn thoát ván cờ hãy gõ 'chess.out'",file=discord.File(fp=load_img(board.fen()), filename="chess.png"))
                
                async def push_san(id, a):
                    board.push_san(str(a).lower())
                    img = load_img(board.fen())
                    await send.edit(content = f"lượt của <@{id}>",attachments=[discord.File(img, filename="chess.png")])
                turn = 1
                while True:
                    if board.is_checkmate() == True or board.is_stalemate() == True:
                        break
                    try:
                        if turn == 1:
                            def check(msg):
                                return msg.channel == ctx.channel and msg.author.id == ctx.author.id            
                            message = await self.bot.wait_for("message", check=check)
                            
                            if str(message.content) == "chess.out":
                                await ctx.reply("ván cờ đã kết thúc")
                                break
                            else:
                                await message.delete()
                                await push_san(id=str(member.id),a=str(message.content).lower().strip(" "))
                            turn = 2
                        elif turn == 2:
                            def check(msg):
                                return msg.channel == ctx.channel and msg.author.id == member.id
                            message = await self.bot.wait_for("message", check=check)
                            
                            if str(message.content) == "chess.out":
                                await ctx.reply("ván cờ đã kết thúc")
                                break
                            else:
                                await message.delete()
                                await push_san(id = str(ctx.message.author.id), a = str(message.content).lower().strip(" "))
                            turn = 1
                    except Exception as e:
                        print(e)
                        await ctx.reply("nước đi không hợp lệ, vui lòng thử lại", delete_after = 3.5)
                        continue
                await ctx.send("Ván đấu đã kết thúc")
            except Exception as e:
                print(e)
    
async def setup(bot):
    await bot.add_cog(Chess(bot))
