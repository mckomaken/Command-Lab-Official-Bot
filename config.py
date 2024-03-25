from pydantic import BaseModel


class BumpNofitication(BaseModel):
    channel_id: int
    disboard_id: int


class Config(BaseModel):
    token: str
    guild_id: int
    administrater_role_id: int
    bump: BumpNofitication
    status: str

# -----------------------------------------------------------


class PackVersionEntry(BaseModel):
    rp: int
    dp: int


class PackVersions(BaseModel):
    versions: dict[str, PackVersionEntry]


config = Config.model_validate_json(
    open("./config.json", mode="rb").read()
)

pack_versions = PackVersions.model_validate_json(
    open("./pack_versions.json").read()
)
