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
