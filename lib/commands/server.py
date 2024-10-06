from typing import Optional, Union
from uuid import UUID
from lib.commands.entity import ServerPlayerEntity
from lib.commands.world import ServerWorld


class PlayerManager:
    players: list[ServerPlayerEntity]

    def __init__(self) -> None:
        self.players = list()

    def getPlayer(self, name_or_uuid: Union[str, UUID]) -> Optional[ServerPlayerEntity]:
        if isinstance(name_or_uuid, str):
            return next(iter([p for p in self.players if p.getName().getString() == name_or_uuid]), None)
        elif isinstance(name_or_uuid, UUID):
            return next(iter([p for p in self.players if p.getUUID() == name_or_uuid]), None)
        else:
            raise TypeError()

    def getPlayerList(self):
        return self.players


class MinecraftServer:
    def __init__(self) -> None:
        self.playerManager = PlayerManager()

    def getPlayerManager(self):
        return self.playerManager

    def getWorlds() -> list[ServerWorld]:
        return []
