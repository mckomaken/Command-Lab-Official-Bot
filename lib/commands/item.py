from lib.commands.registry.registry import Registries


class ItemSettings:
    pass

class Item:
    def __init__(self, settings: ItemSettings) -> None:
        self.registryEntry = Registries.ITEM.createEntry(self)
        self.components = settings.getValidatedComponents()
        self.recipeRemainder = settings.recipeRemainder
        self.requiredFratures = settings.requiredFetatures

    def getComponents(self):
        return self.components