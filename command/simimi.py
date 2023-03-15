import discord
from discord.ext import commands
from discord import *
import aiohttp
import json


class Simimi(commands.Cog):
    config = {
        "name": "simimi",
        "desc": "nói chuyện với trợ lý simimi",
        "use": "simimi <channel>",
        "author": "King.(maku team)"
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.id != self.bot.user.id:
                self.bot.sql.execute(
                    f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
                if (self.bot.sql.fetchone() == None):
                    self.bot.sql.execute(
                        f'INSERT INTO server_data (server_id,server_prefix,server_channel_simimi,server_channel_confession) VALUES ({message.guild.id},0,0,0)')
                else:
                    self.bot.sql.execute(
                        f'SELECT server_channel_simimi FROM server_data WHERE server_id={message.guild.id}')
                    server_channel_simimi = self.bot.sql.fetchone()[0]
                    if message.channel.id == server_channel_simimi:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(
                                    f'https://simsimi.info/api/?lc=vi&text={message.content}') as get_answer:
                                get_answer = await get_answer.text()
                                answer = json.loads(get_answer)
                                if answer["status"] == "success":
                                    await message.reply(answer['message'])
                                else:
                                    await message.reply("oppa nói lại rõ hơn đc khum ạ,em chx hiểu lắm 😳")

            self.bot.database.commit()
        except Exception as e:
            print(e)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def simimi(self, ctx, channel: discord.TextChannel):
        try:
            self.bot.sql.execute(
                f'UPDATE server_data SET server_channel_simimi={channel.id} WHERE server_id={ctx.guild.id}')
            await ctx.reply(f"Đã đổi channel của simimi sang kênh {channel.mention}")
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Simimi(bot))
