from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GamePackageRuleOS(BaseModel):
    name: Optional[str] = ""
    arch: Optional[str] = ""


class GamePackageRule(BaseModel):
    action: str
    os: Optional[GamePackageRuleOS] = None
    features: Optional[dict[str, bool]] = None


class GamePackageJVM(BaseModel):
    rules: Optional[GamePackageRule | list[GamePackageRule]] = None
    value: Optional[str | list[str]] = None


class GamePackageArguments(BaseModel):
    game: list[GamePackageJVM | str]
    jvm: list[GamePackageJVM | str]


class GamePackageAssetIndex(BaseModel):
    id: str
    sha1: str
    size: int
    totalSize: int
    url: str


class GamePackageDownload(BaseModel):
    path: Optional[str] = ""
    sha1: str
    size: int
    url: str


class GamePackageDownloads(BaseModel):
    client: GamePackageDownload
    client_mappings: GamePackageDownload
    server: GamePackageDownload
    server_mappings: GamePackageDownload


class GamePackageJavaVersion(BaseModel):
    component: str
    majorVersion: int


class GamePackageLibrary(BaseModel):
    downloads: dict[str, GamePackageDownload]
    name: str
    rules: Optional[list[GamePackageRule]] = []


class GamePackage(BaseModel):
    arguments: GamePackageArguments
    assetIndex: GamePackageAssetIndex
    assets: str
    complianceLevel: int
    id: str
    downloads: GamePackageDownloads
    libraries: list[GamePackageLibrary]
    mainClass: str
    minimumLauncherVersion: int
    releaseTime: datetime
    time: datetime
    type: str


class AssetIndexEntry(BaseModel):
    hash: str
    size: int


class AssetIndex(BaseModel):
    objects: dict[str, AssetIndexEntry]
