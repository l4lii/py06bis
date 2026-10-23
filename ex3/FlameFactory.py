from .factory import CreatureFactory
from .creature import Creature
from .flameling import Flameling
from .pyrodon import Pyrodon


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()
