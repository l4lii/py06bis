from .factory import CreatureFactory
from .creature import Creature
from .shiftling import Shiftling
from .morphagon import Morphagon


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
