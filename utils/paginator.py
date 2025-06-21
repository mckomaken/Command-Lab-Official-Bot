from __future__ import annotations

import discord
from discord.ext import commands


class EmbedPaginator(discord.ui.View):
    """
    Embed Paginator.
    await EmbedPaginator.start() でpaginateされたembedが送信されます

    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
        最後のinteractionからタイムアウトするまでの時間（秒）（標準は60秒）
    PreviousButton: discord.ui.Button
        Overrides default previous button.
        「前へ」ボタン
    NextButton: discord.ui.Button
        Overrides default next button.
        「次へ」ボタン
    PageCounterStyle: discord.ButtonStyle
        Overrides default page counter style.
        ページ数を表示するボタン
    InitialPage: int
        Page to start the pagination on.
        最初に表示されるページ
    AllowExtInput: bool
        Overrides ability for 3rd party to interract with button.
    """

    def __init__(
        self,
        *,
        timeout: int = 60,
        PreviousButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025c0")
        ),
        NextButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025b6")
        ),
        PageCounterStyle: discord.ButtonStyle = discord.ButtonStyle.grey,
        InitialPage: int = 0,
        AllowExtInput: bool = False,
        ephemeral: bool = False,
    ) -> None:

        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage
        self.AllowExtInput = AllowExtInput
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        super().__init__(timeout=timeout)

    # Embedを送信
    async def start(
        self, ctx: discord.Interaction | commands.Context, pages: list[discord.Embed]
    ):
        """
        await EmbedPaginator.start(ctx, pages)
        paginateされたembedを送信します

        Attributes
        ----------
        ctx: discord.Interaction | commands.Context
        pages: list[discord.Embed]
            ページ一つ一つのembedのリスト
        """

        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback

        self.page_counter = SimplePaginatorPageCounter(
            style=self.PageCounterStyle,
            TotalPages=self.total_page_count,
            InitialPage=self.InitialPage,
        )

        self.add_item(self.PreviousButton)
        self.add_item(self.page_counter)
        self.add_item(self.NextButton)

        self.message = await ctx.send(
            embed=self.pages[self.InitialPage], view=self, ephemeral=self.ephemeral
        )

    # ページを一つ前へ戻す
    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    # ページを一つ後へ送る
    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    # 「次へ」ボタン押下検知
    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.AllowExtInput:
            embed = discord.Embed(
                # 送信者以外は操作できません
                description="You cannot control this pagination because you did not execute it.",
                color=discord.Colour.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    # 「前へ」ボタン押下検知
    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.AllowExtInput:
            embed = discord.Embed(
                # 送信者以外は操作できません
                description="You cannot control this pagination because you did not execute it.",
                color=discord.Colour.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()


class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, TotalPages, InitialPage):
        super().__init__(
            label=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True
        )
