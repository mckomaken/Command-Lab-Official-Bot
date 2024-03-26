import discord


def create_codeblock(data: str):
    return f"```{data}```"


def create_embed(title: str, description: str):
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green()
    )
