import os
from os import path
from typing import Optional

from pydantic import BaseModel

latest_minecraft_data_version = "1.21.4"
latest_version = "1.21.8"


class BumpNofitication(BaseModel):
    channel_id: int
    disboard_id: int


class YChannel(BaseModel):
    channel_id: int
    admin_channel_id: int


class Mee6(BaseModel):
    botch: int
    levelup: int
    levelupnoticeoff: int
    senndennkenn: int
    hanabira: int
    mcmdlv_5: int
    five_5: Optional[int] = 0
    ten_10: Optional[int] = 0
    fifteen_15: Optional[int] = 0
    twenty_20: Optional[int] = 0
    twentyfive_25: Optional[int] = 0
    thirty_30: Optional[int] = 0
    thirtyfive_35: Optional[int] = 0
    forty_40: Optional[int] = 0
    fortyfive_45: Optional[int] = 0
    fifty_50: Optional[int] = 0
    sixty_60: Optional[int] = 0
    seventy_70: Optional[int] = 0
    eighty_80: Optional[int] = 0
    ninety_90: Optional[int] = 0
    onehundred_100: Optional[int] = 0


class Roles(BaseModel):
    beginner: int
    basic: int
    intermediate: int
    advanced: int
    java_edition: int
    bedrock_edition: int
    computer: int
    smartphone: int
    console: int
    server_booster: int
    regular_member: int


class Channels(BaseModel):
    bot_log_channel: Optional[int] = None
    start_notice_channel: Optional[int] = None
    lottery_channel: Optional[int] = None
    y_channel: Optional[int] = None
    advertisement_channnel_id: Optional[int] = None
    bot_command_channel_id: Optional[int] = None
    role_set_channel: Optional[int] = None
    self_introduction_channel: Optional[int] = None
    authentication_channel: Optional[int] = None
    admin_meeting_channel: Optional[int] = None

    voice_channel: Optional[int] = None

    question_channels: list[int] = []


class Config(BaseModel):
    token: str
    guild_id: int
    administrater_role_id: int
    bump: BumpNofitication
    status: str
    enabled_features: list[str] = []
    owner_ids: list[int] = []
    prefix: str = "cm!"
    mee6: Mee6
    roles: Roles
    channels: Channels
    admin_category_id: int
    anotherch: int
    freechat: int
    listench: int
    syunngikuid: int
    listenchs: list[int] = []
    voicech: int
    voice256ch: int
    toiawasech: int
    invite_ch: int


# -----------------------------------------------------------


class PackVersionEntry(BaseModel):
    rp: int
    dp: int


class PackVersions(BaseModel):
    versions: dict[str, PackVersionEntry]


config = Config.model_validate_json(open(path.join(os.getenv("BASE_DIR", "."), "config/config.json"), mode="rb").read())

pack_versions = PackVersions.model_validate_json(open(path.join(os.getenv("BASE_DIR", "."), "data/pack_versions.json")).read())
