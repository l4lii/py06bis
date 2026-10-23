from abc import ABC, abstractmethod
from ex3 import Creature, TransformCapability
from .errors import InvalidStrategyError


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' for this normal strategy"
            )
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}'"
                "for this aggressive strategy"
            )
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())
