from typing import TypeGuard

import discord

TextChannelLike = discord.TextChannel | discord.VoiceChannel | discord.StageChannel


def is_text_channel(channel: discord.abc.MessageableChannel) -> TypeGuard[TextChannelLike]:
    return isinstance(channel, discord.abc.Messageable)

def is_member(user: discord.User)