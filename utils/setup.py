import hashlib
import logging
import os

import aiofiles
import aiohttp

from cogs.cnews import VersionManifest
from schemas.game_package import GamePackage

logger = logging.getLogger("Initialize Process")


async def setup():
    if not os.path.exists("./tmp"):
        logger.warning("tmpフォルダが存在しません。新しく作成します。")
        os.mkdir("./tmp")

    logger.info("バージョン情報をダウンロードしています...")
    async with aiohttp.ClientSession() as client:
        async with client.get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json") as resp1:
            logger.info("バージョン情報の取得が完了しました。")
            version_manifest = VersionManifest.model_validate(await resp1.json())
            logger.info("-------------------------------------------------")
            logger.info(f" 最新リリース: {version_manifest.latest.release}")
            logger.info(f" 最新スナップショット: {version_manifest.latest.snapshot}")
            logger.info("-------------------------------------------------")

            latest_version = version_manifest.latest.release
            url = ""
            logger.info(f"バージョン{latest_version}のclient.jarを使用します。")

            for ver in version_manifest.versions:
                if ver.id == latest_version:
                    url = ver.url

            if url == "":
                return

            async with client.get(url=url) as resp2:
                game_package = GamePackage.model_validate(await resp2.json())
                path = "./tmp/client_" + game_package.id + ".jar"

                if os.path.exists(path):
                    hash = hashlib.sha1(
                        await (await aiofiles.open(path, mode="rb")).read()
                    ).hexdigest()

                    if hash == game_package.downloads.client.sha1:
                        logger.info("client.jarは既にダウンロードされているため、ダウンロードをスキップします。")
                        return
                    else:
                        logger.info("client.jarのハッシュがサーバー上と同期されていません! 再ダウンロードを行います。")

                async with client.get(url=game_package.downloads.client.url) as resp3:
                    async with aiofiles.open(path, mode="wb") as fp:
                        await fp.write(await resp3.read())
                        await fp.close()
                        logger.info("ダウンロードが完了しました!")
