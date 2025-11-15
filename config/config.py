from os import path
import os
from typing import Optional

from pydantic import BaseModel

# -----------------------------------------------------------
# red 削除: BumpNofitication, YChannel, Mee6
# green 維持: Roles, Config
# yellow 新規: Channels, Categories, Users
# blue 旧: administrater_role_id, bump, owner_ids, question_channels, y_channel, cmdbot_log, lottery_channel,
# blue     mee6, advertisement_channnel_id, admin_category_id, botcommand_channel_id, role_set_ch, ninnsyouch,
# blue     selfintroductionch, anotherch, freechat, listench, syunngikuid, voicech, voice256ch, toiawasech, invite_ch, admin_meeting_ch
# red なおこの一覧があってるかはわからない(VSCの自動補完機能使ったからｗ)
# -----------------------------------------------------------

latest_minecraft_data_version = "1.21.4"
latest_version = "1.21.10"


class BumpNofitication(BaseModel):  # red 削除
    channel_id: int
    disboard_id: int


class YChannel(BaseModel):  # red 削除
    channel_id: int
    admin_channel_id: int


class Mee6(BaseModel):  # red 削除
    botch: int  # blue 旧
    levelup: int  # blue 旧
    levelupnoticeoff: int  # blue
    senndennkenn: int  # blue 旧
    hanabira: int  # blue 旧
    mcmdlv_5: int  # blue 旧

# red これらは一旦削除でいいよな？
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


class Roles(BaseModel):  # green 維持
    kakedasi: int  # blue 旧
    newbie: int  # orange 駆け出し

    syokyuu: int  # blue 旧
    beginner: int  # orange 初級

    tyuukyuu: int  # blue 旧
    intermediate: int  # orange 中級

    zyoukyuu: int  # blue 旧
    advanced: int  # orange 上級

    jezei: int  # blue 旧
    java_edition: int  # orange JE勢

    bezei: int  # blue 旧
    bedrock_edition: int  # orange BE勢

    personalcomputer: int  # blue 旧
    computer: int  # orange BE勢

    gamemachine: int  # blue 旧
    console: int  # orange BE勢

    smartphone: int  # green 維持
    serverbooster: int  # green 維持
    regularmember: int  # green 維持

    administrater: int  # orange 管理者
    levelupnoticeoff: int  # orange MEE6レベル通知オフ
    advertising_rights: int  # orange 宣伝権(仮)
    no_advertising: int  # orange 宣伝禁止
    mcmdlv_5: int  # orange MCMDレベル5以上


class Channels():  # yellow 新規
    komaken_bot_development_room: int  # orange コマ研Bot開発室
    question_channels: list[int] = []  # orange 質問チャンネルリスト
    y_channel: int  # orange y談チャンネル
    cmdbot_log: int  # orange コマンドラボBotログチャンネル
    lottery: int  # orange 抽選チャンネル
    level_data: int  # orange レベルデータ送信チャンネル
    levelup: int  # orange レベルアップ通知チャンネル
    advertisement: int  # orange 宣伝チャンネル
    bot_command: int  # orange Botコマンドチャンネル
    role_set: int  # orange ロール設定チャンネル
    authentication: int  # orange 認証問い合わせチャンネル
    selfintroduction: int  # orange 自己紹介チャンネル
    another: int  # orange その他チャンネル(未指定チャンネル)
    freechat: int  # orange 総合雑談チャンネル
    listen: int  # orange 聞き専チャンネル
    voice: int  # orange ボイスチャンネル
    voice256: int  # orange 256kbpsボイスチャンネル
    discord_inquiry: int  # orange Discord問い合わせチャンネル
    invite: int  # orange 入所者チャンネル
    admin_meeting: int  # orange 運営会議チャンネル
    disboard_command: int  # orange Disboardコマンドチャンネル


class Categories(BaseModel):  # yellow 新規
    administrater: int  # orange 管理者カテゴリー


class Users(BaseModel):  # yellow 新規
    owner_ids: list[int] = []  # orange 所有者ID
    syunngiku: int  # orange 春菊ID
    disboard_bot: int  # orange Disboard Bot ID


class Config(BaseModel):
    token: str  # green 維持
    guild_id: int  # green 維持
    administrater_role_id: int  # blue 旧
    bump: BumpNofitication  # blue 旧
    status: str  # green 維持
    start_notice_channel: Optional[int] = None  # green 維持
    enabled_features: list[str] = []  # green 維持
    owner_ids: list[int] = []  # blue 旧
    prefix: Optional[str] = "cm!"  # green 維持
    question_channels: list[int] = []  # blue 旧
    y_channel: int  # blue 旧
    cmdbot_log: int  # blue 旧
    lottery_channel: int  # blue 旧
    mee6: Mee6  # blue 旧
    advertisement_channnel_id: int  # blue 旧
    admin_category_id: int  # blue 旧
    botcommand_channel_id: int  # blue 旧
    role_set_ch: int  # blue 旧
    ninnsyouch: int  # blue 旧
    selfintroductionch: int  # blue 旧
    anotherch: int  # blue 旧
    freechat: int  # blue 旧
    listench: int  # blue 旧
    syunngikuid: int  # blue 旧
    listenchs: list[int] = []  # red 削除
    voicech: int  # blue 旧
    voice256ch: int  # blue 旧
    toiawasech: int  # blue 旧
    invite_ch: int  # blue 旧
    admin_meeting_ch: int  # blue 旧

    roles: Roles  # green 維持
    channels: Channels = Channels()  # yellow 新規
    categories: Categories = Categories()  # yellow 新規
    users: Users = Users()  # yellow 新規

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
