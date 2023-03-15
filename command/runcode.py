import ast
import discord
from discord.ext import commands

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Runcode(commands.Cog):
    config = {
        "name": "runcode",
        "desc": "chạy code online",
        "use": "runcode <code>",
        "author": "...",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def run(self,ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)
        except Exception as e:
            print(e)
            


async def setup(bot):
    await bot.add_cog(Runcode(bot))
    
