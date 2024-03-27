from datetime import datetime

from pydantic import BaseModel


class VersionManifestEntry(BaseModel):
    id: str
    type: str
    url: str
    time: datetime
    releaseTime: datetime
    sha1: str
    complianceLevel: int


class VersionManifestLatest(BaseModel):
    release: str
    snapshot: str


class VersionManifest(BaseModel):
    latest: VersionManifestLatest
    versions: list[VersionManifestEntry]
