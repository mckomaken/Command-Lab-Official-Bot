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
    sha1: Optional[str] = ""
    size: Optional[int] = 0
    url: Optional[str] = ""


class GamePackageDownloads(BaseModel):
    client: GamePackageDownload
    client_mappings: Optional[GamePackageDownload] = None
    server: GamePackageDownload
    server_mappings: Optional[GamePackageDownload] = None


class GamePackageJavaVersion(BaseModel):
    component: str
    majorVersion: int


class GamePackageLibrary(BaseModel):
    downloads: dict[str, GamePackageDownload]
    name: str
    rules: Optional[list[GamePackageRule]] = []


class GamePackage(BaseModel):
    arguments: Optional[GamePackageArguments] = None
    assetIndex: GamePackageAssetIndex
    assets: str
    complianceLevel: Optional[int] = 0
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
