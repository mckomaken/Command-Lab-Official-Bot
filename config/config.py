from os import path
import os
from typing import Optional

from pydantic import BaseModel

latest_minecraft_data_version = "1.21.4"
latest_version = "1.21.11"


class Roles(BaseModel):
    newbie: int  # 駆け出し
    beginner: int  # 初級
    intermediate: int  # 中級
    advanced: int  # 上級
    java_edition: int  # JE勢
    bedrock_edition: int  # BE勢
    computer: int  # PC勢
    smartphone: int  # スマホ勢
    console: int  # コンソール勢
    administrater: int  # 管理者
    regularmember: int  # 正規メンバー
    serverbooster: int  # サーバーBooster
    levelupnoticeoff: int  # MEE6レベル通知オフ
    advertising_rights: int  # 宣伝権(仮)
    no_advertising: int  # 宣伝禁止
    mcmd_5lv: int  # yellow MCMDレベル5以上 コンフィグ名変更
    mcmd_10lv: int  # yellow MCMDレベル10以上 新規
    mcmd_20lv: int  # yellow MCMDレベル20以上 新規
    mcmd_30lv: int  # yellow MCMDレベル30以上 新規
    mcmd_300lv: int  # yellow MCMDレベル300以上 新規
    mcmd_600lv: int  # yellow MCMDレベル600以上 新規
    mcmd_1000lv: int  # yellow MCMDレベル1000以上 新規


class Channels(BaseModel):
    invite: int  # 入所者チャンネル
    selfintroduction: int  # 自己紹介チャンネル
    role_set: int  # ロール設定チャンネル
    lottery: int  # 抽選チャンネル

    question_channels: list[int] = []  # 質問チャンネルリスト

    freechat: int  # 総合雑談チャンネル
    y_channel: int  # y談チャンネル
    listen: int  # 聞き専チャンネル
    voice: int  # ボイスチャンネル
    voice256: int  # 256kbpsボイスチャンネル

    komaken_bot_development_room: int  # コマ研Bot開発室

    advertisement: int  # 宣伝チャンネル

    bot_command: int  # Botコマンドチャンネル
    disboard_command: int  # Disboardコマンドチャンネル
    levelup: int  # レベルアップ通知チャンネル

    discord_inquiry: int  # Discord問い合わせチャンネル

    admin_meeting: int  # 運営会議チャンネル
    cmdbot_log: int  # コマ研Botログチャンネル
    level_data: int  # レベルデータ送信チャンネル

    authentication: int  # 認証問い合わせチャンネル

    another: int  # その他チャンネル(未指定チャンネル)


class Categories(BaseModel):
    administrater: int  # 管理者カテゴリー


class Users(BaseModel):
    owner_ids: list[int] = []  # 鯖主ID
    syunngiku: int  # 春菊ID
    disboard_bot: int  # Disboard Bot ID


class Config(BaseModel):
    token: str
    guild_id: int
    status: str
    start_notice_channel: Optional[int] = None
    enabled_features: list[str] = []
    prefix: Optional[str] = "cm!"
    roles: Roles
    channels: Channels
    categories: Categories
    users: Users

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
