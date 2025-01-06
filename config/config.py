from os import path
import os
from typing import Optional

from pydantic import BaseModel

latest_version = "1.21.1"


class BumpNofitication(BaseModel):
    channel_id: int
    disboard_id: int


class YChannel(BaseModel):
    channel_id: int
    admin_channel_id: int


class MEe6(BaseModel):
    botch: int
    levelup: int
    levelupnoticeoff: int
    five_5: int
    ten_10: int
    fifteen_15: int
    twenty_20: int
    twenty_25: int
    twenty_30: int
    twenty_35: int
    twenty_40: int
    twenty_45: int
    twenty_50: int
    twenty_60: int
    twenty_70: int
    twenty_80: int
    twenty_90: int
    twenty_100: int



class Config(BaseModel):
    token: str
    guild_id: int
    administrater_role_id: int
    bump: BumpNofitication
    status: str
    start_notice_channel: Optional[int] = None
    enabled_features: list[str] = []
    owner_ids: list[int] = []
    prefix: Optional[str] = "cm!"
    question_channels: list[int] = []
    y_channel: int
    cmdbot_log: int
    lottery_channel: int
    mee6: MEe6
    advertisement_channnel_id: int
    admin_category_id: int
    botcommand_channel_id: int

# -----------------------------------------------------------


class PackVersionEntry(BaseModel):
    rp: int
    dp: int


class PackVersions(BaseModel):
    versions: dict[str, PackVersionEntry]


config = Config.model_validate_json(open(path.join(os.getenv("BASE_DIR", "."), "config/config.json"), mode="rb").read())

pack_versions = PackVersions.model_validate_json(
    open(path.join(os.getenv("BASE_DIR", "."), "data/pack_versions.json")).read()
)
