import hashlib
import logging
import os
from datetime import datetime
from typing import Optional

import aiofiles
import aiohttp
import pygit2
from pydantic import BaseModel
from tqdm import tqdm

from cogs.cnews import VersionManifest
from config import config
from schemas.game_package import AssetIndex, GamePackage

logger = logging.getLogger("Initialize Process")


class ProgressBar(pygit2.RemoteCallbacks):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def transfer_progress(self, stats):
        self.pbar.total = stats.total_objects
        self.pbar.n = stats.indexed_objects
        self.pbar.refresh()


async def setup():
    if not os.path.exists(os.getenv("TMP_DIRECTORY", "./.tmp")):
        logger.warning("tmpフォルダが存在しません。新しく作成します。")
        os.mkdir(os.getenv("TMP_DIRECTORY", "./.tmp"))

    logger.info("バージョン情報をダウンロードしています...")
    async with aiohttp.ClientSession() as client:
        async with client.get(
            "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        ) as resp1:
            logger.info("バージョン情報の取得が完了しました。")
            version_manifest = VersionManifest.model_validate(await resp1.json())
            logger.info("-------------------------------------------------")
            logger.info(f" 最新リリース: {version_manifest.latest.release}")
            logger.info(f" 最新スナップショット: {version_manifest.latest.snapshot}")
            logger.info("-------------------------------------------------")

            latest_version = version_manifest.latest.release
            config.latest_version = latest_version
            url = ""
            logger.info(f"バージョン{latest_version}のclient.jarを使用します。")

            for ver in version_manifest.versions:
                if ver.id == latest_version:
                    url = ver.url

            if url == "":
                return

            async with client.get(url=url) as resp2:
                game_package = GamePackage.model_validate(await resp2.json())
                path = os.path.join(
                    os.getenv("TMP_DIRECTORY", "./.tmp"),
                    "client_" + game_package.id + ".jar",
                )

                logger.info("言語ファイルをダウンロードしています...")
                async with client.get(url=game_package.assetIndex.url) as resp4:
                    asset_index = AssetIndex.model_validate(await resp4.json())
                    lang_file_hash = asset_index.objects[
                        "minecraft/lang/ja_jp.json"
                    ].hash
                    async with client.get(
                        f"https://resources.download.minecraft.net/{lang_file_hash[0:2]}/{lang_file_hash}"
                    ) as resp5:
                        async with aiofiles.open(
                            os.path.join(
                                os.getenv("TMP_DIRECTORY", "./.tmp"), "ja_jp.json"
                            ),
                            mode="wb",
                        ) as fp2:
                            lang_data = await resp5.text()
                            await fp2.write(lang_data.encode())
                            await fp2.close()
                logger.info("言語ファイルのダウンロードが完了しました!")

                if os.path.exists(path):
                    hash = hashlib.sha1(
                        await (await aiofiles.open(path, mode="rb")).read()
                    ).hexdigest()

                    if hash == game_package.downloads.client.sha1:
                        logger.info(
                            "client.jarは既にダウンロードされているため、ダウンロードをスキップします。"
                        )
                        return
                    else:
                        logger.info(
                            "client.jarのハッシュがサーバー上と同期されていません! 再ダウンロードを行います。"
                        )

                async with client.get(url=game_package.downloads.client.url) as resp3:
                    async with aiofiles.open(path, mode="wb") as fp:
                        await fp.write(await resp3.read())
                        await fp.close()
                        logger.info("ダウンロードが完了しました!")


async def setup_mcdata():
    if not os.path.exists("./minecraft_data"):
        logger.info("Githubからデータをダウンロードしています...")
        pygit2.clone_repository(
            "https://github.com/PrismarineJS/minecraft-data.git",
            "minecraft_data",
            callbacks=ProgressBar(),
        )


class VersionDataPackFormat(BaseModel):
    resource: Optional[int] = None
    data: Optional[int] = None


class VersionData(BaseModel):
    id: str
    name: str
    world_version: int
    series_id: str
    protocol_version: int
    pack_version: VersionDataPackFormat
    build_time: datetime
    java_component: str
    java_version: int
    stable: bool
