from __future__ import annotations

from discord.ext.commands import (
    HelpCommand as _HelpCMD,
    Cog, Command, Bot,
    Context
)
from typing import Mapping, Optional, List, Any, Union
from discord import (
    Embed, User, Member, Message, Interaction, InteractionResponse
)
from discord.ui import (
    Button, View,
    button
)


class HelpBotView(View):
    def __init__(self, ctx: Context, embeds: List[Embed]):
        super().__init__(timeout=60)

        self.ctx = ctx
        self.embeds = embeds
        self.message: Optional[Message] = None
        self.ptr = 0

    @property
    def now_page(self) -> Embed:
        return self.embeds[self.ptr]

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)

    async def start(self):
        self.check_buttons()
        self.message = await self.ctx.send(embed=self.now_page, view=self)

    def check_buttons(self):
        self._first_page.disabled = self._previous_page.disabled = self.ptr == 0
        self._next_page.disabled = self._last_page.disabled = self.ptr == len(self.embeds) - 1

    async def process(self, itr: Interaction):
        self.check_buttons()
        await itr.response.edit_message(embed=self.now_page, view=self)

    @button(label='<<')
    async def _first_page(self, itr: Interaction, btn: Button):
        self.ptr = 0
        await self.process(itr)

    @button(label='<')
    async def _previous_page(self, itr: Interaction, btn: Button):
        self.ptr -= 1
        await self.process(itr)

    @button(label='>')
    async def _next_page(self, itr: Interaction, btn: Button):
        self.ptr += 1
        await self.process(itr)

    @button(label='>>')
    async def _last_page(self, itr: Interaction, btn: Button):
        self.ptr = len(self.embeds) - 1
        await self.process(itr)


class HelpCommand(_HelpCMD):
    @property
    def bot(self) -> Bot:
        return self.context.bot

    @property
    def author(self) -> Union[User, Member]:
        return self.context.author

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command[Any, ..., Any]]], /) -> None:
        ctx = self.context
        await ctx.typing()

        embeds = []
        embed = Embed()
        c = 1

        for cog, commands in mapping.items():
            commands = await self.filter_commands(commands)

            if not commands:
                continue

            data = getattr(cog, 'config', {})
            name = data.get('name', commands[0].qualified_name)
            description = data.get('desc', '\u200b')

            embed.add_field(
                name=f'{ctx.clean_prefix}{name}',
                value=description
            )

            if c % 9 == 0:
                embed.set_footer(text=f'Page: {c // 9}')
                embeds.append(embed)
                embed = Embed()

            c += 1

        embed.set_footer(text=f'Page: {len(embeds) + 1}')
        embeds.append(embed)

        for embed in embeds:
            embed.set_footer(text=embed.footer.text + f'/{len(embeds)}')

        await HelpBotView(ctx, embeds).start()

    async def on_help_command_error(self, ctx, error) -> None:
        await ctx.send(str(error))

    async def _embed_command_help(self, command: Command):
        ctx = self.context
        data = getattr(command.cog, 'config', {
            'name': command.qualified_name,
            'author': 'Unknown',
            'use': f'{command.qualified_name} {command.signature}',

        })

        cd = command.cooldown

        embed = Embed(
            title=f'{ctx.clean_prefix}{data["name"]}',
            description=data.get('desc', '')
        ).set_author(
            name=f'Creator: {data["author"]}'
        ).add_field(
            name='Usage',
            value=f'{ctx.clean_prefix}{data["use"]}',
            inline=False
        ).add_field(
            name='Cooldown',
            value=f'{cd.rate} lệnh / {cd.per :.2f} giây.' if cd else '0s'
        ).set_footer(text=self.author, icon_url=self.author.display_avatar)

        return embed

    async def send_command_help(self, command: Command[Any, ..., Any], /) -> None:
        await self.context.reply(embed=await self._embed_command_help(command))


class Help(Cog):
    config = {
        "name": "help",
        "desc": "Xem các lệnh của bot.",
        "use": "help <command>",
        "author": "si23"
    }

    def __init__(self, bot: Bot):
        self.bot = bot
        self._original_help = bot.help_command

        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    async def cog_unload(self) -> None:
        self.bot.help_command = self._original_help


async def setup(bot):
    await bot.add_cog(Help(bot))
